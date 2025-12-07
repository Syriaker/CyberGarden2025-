from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from wishes.models import WishItem, Notification


class Command(BaseCommand):
    help = 'Проверяет желания и отправляет уведомления'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        self.stdout.write(f"Запуск проверки уведомлений: {now}")

        wishes = WishItem.objects.filter(status='cooling')

        for wish in wishes:
            if wish.cooling_end_date and now >= wish.cooling_end_date:
                wish.status = 'ready'
                wish.save()

                msg = f"Поздравляем! Период охлаждения для '{wish.title}' прошел. Если вы все еще хотите это — покупайте!"

                if wish.notify_on_end:
                    self.send_email(wish.user, "Время пришло!", msg)

                Notification.objects.create(user=wish.user, message=msg)

                self.stdout.write(self.style.SUCCESS(f"Готово к покупке: {wish.title}"))
                continue

            if wish.report_frequency != 'none':
                should_notify = False
                last_sent = wish.last_notification_sent or wish.created_at
                delta = now - last_sent

                if wish.report_frequency == 'daily' and delta.days >= 1:
                    should_notify = True
                elif wish.report_frequency == 'weekly' and delta.days >= 7:
                    should_notify = True
                elif wish.report_frequency == 'monthly' and delta.days >= 30:
                    should_notify = True

                if should_notify:
                    days_left = (wish.cooling_end_date - now).days
                    msg = f"Напоминание: '{wish.title}' все еще в списке желаний. Осталось ждать: {days_left} дн. Ты не передумал?"

                    self.send_email(wish.user, f"Напоминание о {wish.title}", msg)
                    Notification.objects.create(user=wish.user, message=msg)

                    wish.last_notification_sent = now
                    wish.save()
                    self.stdout.write(f"Отправлено напоминание: {wish.title}")

    def send_email(self, user_profile, subject, body):
        email_addr = user_profile.email

        if not email_addr:
            self.stdout.write(self.style.WARNING(f"Пропуск отправки для {user_profile.nickname}: нет email"))
            return
        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [email_addr],
                fail_silently=False,
            )
            self.stdout.write(f"Письмо отправлено на {email_addr}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка отправки почты: {e}"))