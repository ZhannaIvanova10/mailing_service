from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mailing.models import Mailing, Client, Message
from users.models import User


class Command(BaseCommand):
    help = 'Создание групп и назначение прав'

    def handle(self, *args, **kwargs):
        # Создаем группу менеджеров
        manager_group, created = Group.objects.get_or_create(name='Менеджеры')

        if created:
            # Добавляем права на просмотр всех рассылок, клиентов и сообщений
            content_types = [
                ContentType.objects.get_for_model(Mailing),
                ContentType.objects.get_for_model(Client),
                ContentType.objects.get_for_model(Message),
                ContentType.objects.get_for_model(User),
            ]

            permissions = Permission.objects.filter(
                content_type__in=content_types,
                codename__in=[
                    'view_all_mailings',
                    'deactivate_mailing',
                    'view_all_clients',
                    'view_all_messages',
                    'block_user',
                ]
            )

            manager_group.permissions.set(permissions)
            self.stdout.write(self.style.SUCCESS('Группа "Менеджеры" создана'))
        else:
            self.stdout.write('Группа "Менеджеры" уже существует')
