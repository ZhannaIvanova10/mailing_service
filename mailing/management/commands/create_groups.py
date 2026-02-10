from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mailing.models import Mailing, Client, Message
from users.models import User


class Command(BaseCommand):
    help = 'Создает группы пользователей и назначает права'

    def handle(self, *args, **kwargs):
        # Создаем группу "Менеджеры"
        managers_group, created = Group.objects.get_or_create(name='Менеджеры')

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Менеджеры" создана'))

            # Добавляем права
            permissions = []

            # Права для моделей рассылок
            content_type = ContentType.objects.get_for_model(Mailing)
            permissions.extend(Permission.objects.filter(
                content_type=content_type,
                codename__in=['can_view_all_mailings', 'can_disable_mailing']
            ))

            # Права для клиентов
            content_type = ContentType.objects.get_for_model(Client)
            permissions.extend(Permission.objects.filter(
                content_type=content_type,
                codename='can_view_all_clients'
            ))

            # Права для сообщений
            content_type = ContentType.objects.get_for_model(Message)
            permissions.extend(Permission.objects.filter(
                content_type=content_type,
                codename='can_view_all_messages'
            ))

            # Права для пользователей
            content_type = ContentType.objects.get_for_model(User)
            permissions.extend(Permission.objects.filter(
                content_type=content_type,
                codename__in=['can_view_all', 'can_block_user']
            ))

            # Назначаем права группе
            managers_group.permissions.set(permissions)
            self.stdout.write(self.style.SUCCESS(f'Назначено {len(permissions)} прав группе "Менеджеры"'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Менеджеры" уже существует'))
