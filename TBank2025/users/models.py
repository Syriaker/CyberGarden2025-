from django.db import models


class UserProfile(models.Model):
    nickname = models.CharField(
        max_length=50,
        unique=True,
        primary_key=True,
        verbose_name="Никнейм пользователя"
    )

    current_savings = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Текущие накопления"
    )

    monthly_savings = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Сколько откладывает в месяц"
    )

    monthly_spendings = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Сколько тратит в месяц"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"