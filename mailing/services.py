# mailing/services.py
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Mailing, MailingAttempt


def send_mailing(mailing_id):
    try:
        mailing = Mailing.objects.get(pk=mailing_id)
    except Mailing.DoesNotExist:
        raise ValueError(f'Рассылка #{mailing_id} не найдена')

    now = timezone.now()
    if now < mailing.start_time:
        raise ValueError(f'Отправка запрещена: рассылка начнётся {mailing.start_time:%d.%m.%Y %H:%M}')
    if now > mailing.end_time:
        raise ValueError(f'Отправка запрещена: рассылка завершилась {mailing.end_time:%d.%m.%Y %H:%M}')

    recipients = mailing.recipients.all()
    if not recipients:
        raise ValueError('У рассылки нет получателей')

    attempts = []
    for client in recipients:
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email],
                fail_silently=False,
            )
            attempts.append(MailingAttempt(mailing=mailing, status='success', server_response='OK'))
            print(f"✅ Отправлено: {client.email}")
        except Exception as e:
            attempts.append(MailingAttempt(mailing=mailing, status='failed', server_response=str(e)))
            print(f"❌ Ошибка для {client.email}: {e}")

    MailingAttempt.objects.bulk_create(attempts)
    print(f"📦 Создано попыток: {len(attempts)}")
    mailing.update_status()


def send_confirmation_email(user, request):
    token = user.pk
    confirm_url = request.build_absolute_uri(f'/confirm-email/{token}/')
    send_mail(
        subject='Подтверждение email',
        message=f'Здравствуйте, {user.username}!\n\nПодтвердите email:\n{confirm_url}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
    print(f"📧 Письмо отправлено на {user.email}")
