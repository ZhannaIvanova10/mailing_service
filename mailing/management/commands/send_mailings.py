from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from mailing.models import Mailing, MailingAttempt


class Command(BaseCommand):
    help = 'Отправка активных рассылок'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        active_mailings = Mailing.objects.filter(
            start_time__lte=now,
            end_time__gte=now,
            is_active=True,
            status='started'
        )

        for mailing in active_mailings:
            self.stdout.write(f'Отправка рассылки #{mailing.id}')
            self.send_mailing(mailing)

    def send_mailing(self, mailing):
        """Отправка одной рассылки"""
        recipients = mailing.recipients.all()
        sent_count = 0
        error_count = 0

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
                    mailing=mailing,
                    status='success',
                    server_response='Письмо успешно отправлено'
                )
                sent_count += 1

            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status='failure',
                    server_response=str(e)
                )
                error_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Рассылка #{mailing.id}: отправлено {sent_count}, ошибок {error_count}')
        )
