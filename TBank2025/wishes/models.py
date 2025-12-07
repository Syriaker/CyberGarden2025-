from django.db import models

class WishItem(models.Model):
    STATUS_CHOICES = [
        ('cooling', 'Охлаждение'),
        ('ready', 'Можно покупать'),
        ('bought', 'Куплено'),
        ('cancelled', 'Передумал'),
    ]

    FREQUENCY_CHOICES = [
        ('none', 'Не напоминать'),
        ('daily', 'Каждый день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ]

    user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='wishes')
    title = models.CharField("Название", max_length=200)
    price = models.DecimalField("Цена", max_digits=12, decimal_places=2)
    category = models.CharField("Категория", max_length=100, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='cooling')
    created_at = models.DateTimeField(auto_now_add=True)
    cooling_end_date = models.DateTimeField("Дата окончания", null=True, blank=True)

    notify_on_end = models.BooleanField("Уведомить по окончании", default=True)
    report_frequency = models.CharField("Частота отчетов", max_length=20, choices=FREQUENCY_CHOICES, default='weekly')
    last_notification_sent = models.DateTimeField("Дата последнего уведомления", null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.user.nickname})"

    class Meta:
        verbose_name = "Желание"
        verbose_name_plural = "Желания"
        ordering = ['-created_at']

class Notification(models.Model):
    user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField("Текст сообщения")
    is_read = models.BooleanField("Прочитано", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Уведомление"
        ordering = ['-created_at']