# mailing/views.py
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Client, Message, Mailing, MailingAttempt, User
from .forms import ClientForm, MessageForm, MailingForm, UserRegisterForm, UserLoginForm
from .services import send_mailing, send_confirmation_email


# ✅ Миксин: фильтрация queryset по владельцу
class OwnerQuerysetMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Менеджеры').exists():
            return queryset
        return queryset.filter(owner=user)


# ✅ Миксин: доступ только владельцу/менеджеру
class OwnerOrManagerMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Менеджеры').exists():
            return True
        return obj.owner == user


@method_decorator(cache_page(60 * 5), name='dispatch')
class HomeView(TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status='started').count()
        context['unique_recipients'] = Client.objects.count()
        return context


# ===== Client CRUD =====
class ClientListView(LoginRequiredMixin, OwnerQuerysetMixin, ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    context_object_name = 'client_list'
    login_url = 'mailing:login'


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')
    login_url = 'mailing:login'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, OwnerOrManagerMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')
    login_url = 'mailing:login'


class ClientDeleteView(LoginRequiredMixin, OwnerOrManagerMixin, DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')
    login_url = 'mailing:login'


# ===== Message CRUD =====
class MessageListView(LoginRequiredMixin, OwnerQuerysetMixin, ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'message_list'
    login_url = 'mailing:login'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')
    login_url = 'mailing:login'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, OwnerOrManagerMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')
    login_url = 'mailing:login'


class MessageDeleteView(LoginRequiredMixin, OwnerOrManagerMixin, DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')
    login_url = 'mailing:login'


# ===== Mailing CRUD =====
class MailingListView(LoginRequiredMixin, OwnerQuerysetMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailing_list'
    login_url = 'mailing:login'

    def get_queryset(self):
        queryset = super().get_queryset()
        for mailing in queryset:
            mailing.update_status()
        return queryset


class MailingDetailView(LoginRequiredMixin, OwnerQuerysetMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'
    login_url = 'mailing:login'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    login_url = 'mailing:login'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, OwnerOrManagerMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    login_url = 'mailing:login'


class MailingDeleteView(LoginRequiredMixin, OwnerOrManagerMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')
    login_url = 'mailing:login'


# ✅ Отправка — только авторизованный владелец или суперпользователь
@login_required
@require_POST
def send_mailing_view(request, pk):
    queryset = Mailing.objects.all()
    if not request.user.is_superuser:
        queryset = queryset.filter(owner=request.user)

    mailing = get_object_or_404(queryset, pk=pk)

    try:
        send_mailing(mailing.pk)
        messages.success(request, f'Рассылка #{pk} отправлена')
    except ValueError as error:
        messages.error(request, str(error))
    except Exception as error:
        messages.error(request, f'Ошибка: {error}')

    return redirect('mailing:mailing_list')


# ===== Аутентификация =====
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'mailing/register.html'
    success_url = reverse_lazy('mailing:login')

    def form_valid(self, form):
        form.instance.is_active = False  # ✅ неактивен до подтверждения
        response = super().form_valid(form)
        send_confirmation_email(self.object, self.request)
        messages.success(self.request, 'Проверьте почту и подтвердите регистрацию.')
        return response


def confirm_email(request, token):
    from django.core import signing
    from django.core.signing import BadSignature, SignatureExpired

    try:
        user_id = signing.loads(token, max_age=86400)  # 24 часа
    except SignatureExpired:
        return HttpResponse('<h1>❌ Ссылка истекла</h1><a href="/login/">Войти</a>')
    except BadSignature:
        return HttpResponse('<h1>❌ Неверная ссылка</h1><a href="/login/">Войти</a>')

    user = get_object_or_404(User, pk=user_id)
    user.is_active = True
    user.is_email_confirmed = True
    user.save()

    return HttpResponse('<h1>✅ Email подтверждён!</h1><a href="/login/">Войти</a>')


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'mailing/login.html'

    def get_success_url(self):
        return reverse_lazy('mailing:home')


# ===== Статистика =====
@method_decorator(cache_page(60 * 5), name='dispatch')
class StatisticsView(LoginRequiredMixin, TemplateView):
    template_name = 'mailing/statistics.html'
    login_url = 'mailing:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_superuser or user.groups.filter(name='Менеджеры').exists():
            mailings = Mailing.objects.all()
        else:
            mailings = Mailing.objects.filter(owner=user)

        attempts = MailingAttempt.objects.filter(mailing__in=mailings)
        context['total_attempts'] = attempts.count()
        context['success_attempts'] = attempts.filter(status='success').count()
        context['failed_attempts'] = attempts.filter(status='failed').count()
        context['total_messages'] = attempts.filter(status='success').count()
        return context


# ===== Менеджерские функции =====
class ManagerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return (
            self.request.user.is_superuser
            or self.request.user.groups.filter(name='Менеджеры').exists()
        )


class UserListView(ManagerRequiredMixin, ListView):
    model = User
    template_name = 'mailing/user_list.html'
    context_object_name = 'users'
    login_url = 'mailing:login'


def toggle_user_block(request, pk):
    if not (
        request.user.is_superuser
        or request.user.groups.filter(name='Менеджеры').exists()
    ):
        raise PermissionDenied('Доступ запрещён')

    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        status_text = 'разблокирован' if user.is_active else 'заблокирован'
        messages.success(request, f'Пользователь {user.email} {status_text}')

    return redirect('mailing:user_list')


def toggle_mailing(request, pk):
    if not (
        request.user.is_superuser
        or request.user.groups.filter(name='Менеджеры').exists()
    ):
        raise PermissionDenied('Доступ запрещён')

    mailing = get_object_or_404(Mailing, pk=pk)

    if request.method == 'POST':
        if mailing.status == 'started':
            mailing.status = 'completed'
        else:
            mailing.status = 'started'
        mailing.save()
        messages.success(request, f'Статус рассылки #{mailing.pk} изменён')

    return redirect('mailing:mailing_list')
