from django.utils import timezone
from datetime import timedelta


def calculate_cooling_date(price, user_profile):

    # крч, пока что тут заглушка
    days_to_wait = int(price / 5000)
    if days_to_wait < 1:
        days_to_wait = 1

    end_date = timezone.now() + timedelta(days=days_to_wait)

    return end_date, days_to_wait