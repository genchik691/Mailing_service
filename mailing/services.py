# mailing/services.py
from django.core.mail import send_mail
from django.conf import settings
from .models import Mailing, MailingAttempt


def send_mailing(mailing_id):
    try:
        mailing = Mailing.objects.get(pk=mailing_id)
    except Mailing.DoesNotExist:
        print(f"❌ Рассылка #{mailing_id} не найдена")
        return

    recipients = mailing.recipients.all()
    if not recipients:
        print(f"⚠️ У рассылки #{mailing_id} нет получателей")
        return

    for client in recipients:
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email],
                fail_silently=False,
            )
            MailingAttempt.objects.create(
                mailing=mailing, status='success', server_response='OK'
            )
            print(f"✅ Отправлено: {client.email}")
        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing, status='failed', server_response=str(e)
            )
            print(f"❌ Ошибка для {client.email}: {e}")

    if mailing.status == 'created':
        mailing.status = 'started'
        mailing.save()
