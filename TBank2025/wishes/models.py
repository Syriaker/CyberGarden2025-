from django.db import models
from users.models import UserProfile


class WishItem(models.Model):
    STATUS_CHOICES = [
        ('cooling', 'Охлаждение'),
        ('ready', 'Можно покупать'),
        ('bought', 'Куплено'),
        ('cancelled', 'Передумал'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='wishes')

    title = models.CharField("Название", max_length=200)
    price = models.DecimalField("Цена", max_digits=12, decimal_places=2)
    category = models.CharField("Категория", max_length=100, blank=True)
    image_url = models.URLField("Ссылка на картинку", blank=True, null=True)  # todo
    link_url = models.URLField("Ссылка на товар", blank=True, null=True)  # todo

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='cooling')
    created_at = models.DateTimeField(auto_now_add=True)
    cooling_end_date = models.DateTimeField("Дата окончания охлаждения", null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.user.nickname})"

    class Meta:
        verbose_name = "Желание"
        verbose_name_plural = "Желания"
        ordering = ['-created_at']