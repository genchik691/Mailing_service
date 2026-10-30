# mailing/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Client, Message, Mailing, MailingAttempt, User


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'owner')
    search_fields = ('email', 'full_name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'status', 'start_time', 'end_time', 'owner')
    list_filter = ('status',)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing', 'status', 'attempt_time')
    list_filter = ('status',)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'username', 'is_email_confirmed', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('is_email_confirmed',)}),
    )
