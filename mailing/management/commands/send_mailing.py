# mailing/management/commands/send_mailing.py
from django.core.management.base import BaseCommand
from mailing.services import send_mailing


class Command(BaseCommand):
    help = 'Отправляет рассылку по ID'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID рассылки')

    def handle(self, *args, **options):
        mailing_id = options['mailing_id']
        self.stdout.write(f"📨 Запуск рассылки #{mailing_id}...")
        try:
            send_mailing(mailing_id)
            self.stdout.write(self.style.SUCCESS("✅ Готово"))
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f"❌ {e}"))
