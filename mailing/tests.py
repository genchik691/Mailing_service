# mailing/tests.py
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Client, Message, Mailing, MailingAttempt
from .services import send_mailing

User = get_user_model()


class MailingServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.ru', username='test', password='test12345'
        )
        self.client_obj = Client.objects.create(
            email='client@test.ru', full_name='Тест Клиент', owner=self.user
        )
        self.message = Message.objects.create(
            subject='Тема', body='Тело', owner=self.user
        )

    def test_send_before_start_raises(self):
        mailing = Mailing.objects.create(
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=2),
            message=self.message,
            owner=self.user,
        )
        mailing.recipients.add(self.client_obj)
        with self.assertRaises(ValueError):
            send_mailing(mailing.pk)

    def test_send_after_end_raises(self):
        mailing = Mailing.objects.create(
            start_time=timezone.now() - timedelta(days=2),
            end_time=timezone.now() - timedelta(days=1),
            message=self.message,
            owner=self.user,
        )
        mailing.recipients.add(self.client_obj)
        with self.assertRaises(ValueError):
            send_mailing(mailing.pk)

    def test_send_in_window_creates_attempt(self):
        mailing = Mailing.objects.create(
            start_time=timezone.now() - timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=1),
            message=self.message,
            owner=self.user,
        )
        mailing.recipients.add(self.client_obj)
        send_mailing(mailing.pk)
        self.assertEqual(MailingAttempt.objects.filter(mailing=mailing).count(), 1)


class AccessControlTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='u1@test.ru', username='u1', password='pass12345'
        )
        self.user2 = User.objects.create_user(
            email='u2@test.ru', username='u2', password='pass12345'
        )
        self.client1 = Client.objects.create(
            email='c1@test.ru', full_name='Клиент 1', owner=self.user1
        )

    def test_anonymous_redirected_from_send(self):
        mailing = Mailing.objects.create(
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            message=Message.objects.create(subject='S', body='B', owner=self.user1),
            owner=self.user1,
        )
        response = self.client.post(reverse('mailing:mailing_send', args=[mailing.pk]))
        self.assertEqual(response.status_code, 302)

    def test_user_cannot_see_other_client(self):
        self.client.login(email='u2@test.ru', password='pass12345')
        response = self.client.get(reverse('mailing:client_update', args=[self.client1.pk]))
        self.assertEqual(response.status_code, 403)
