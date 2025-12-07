import math
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone


def calculate_cooling_data(price: Decimal, user_profile, category_name: str = ""):
    is_banned = False
    warning_message = None

    if user_profile.blacklisted_categories and category_name:
        banned_list = [x.strip().lower() for x in user_profile.blacklisted_categories.split(',') if x.strip()]
        current_cat = category_name.strip().lower()

        for banned in banned_list:
            if banned and banned in current_cat:
                is_banned = True
                warning_message = f"Категория '{category_name}' в вашем черном списке!"
                print(warning_message)
                break

    if price <= 15000:
        t_static = 1
    elif price <= 50000:
        t_static = 7
    elif price <= 100000:
        t_static = 30
    else:
        t_static = 90

    current_savings = user_profile.current_savings
    monthly_savings = user_profile.monthly_savings

    safety_buffer = current_savings * Decimal(0.5)  # 50%
    available_cash = current_savings - safety_buffer

    if available_cash < 0:
        available_cash = Decimal(0)

    if monthly_savings <= 0:
        t_dynamic = 0
    else:
        daily_savings = monthly_savings / Decimal(30)

        if available_cash >= price:
            t_dynamic = 0
        else:
            needed = price - available_cash
            t_dynamic = math.ceil(needed / daily_savings)

    final_days = max(t_static, t_dynamic)

    if is_banned:
        final_days = 9999

    now = timezone.now()
    end_date = now + timedelta(days=final_days)

    notification_schedule = []
    if final_days > 0 and not is_banned:
        for percent in [25, 50, 75, 100]:
            day_offset = math.ceil(final_days * (percent / 100))
            notify_date = now + timedelta(days=day_offset)

            msg = ""
            if percent == 25:
                msg = "Прошла четверть пути. Ты еще хочешь это?"
            elif percent == 50:
                msg = "Половина срока позади. Может, ну его?"
            elif percent == 75:
                msg = "Почти у цели. Точно будешь брать?"
            elif percent == 100:
                msg = "Срок вышел. Решайся!"

            notification_schedule.append({
                "percent": percent,
                "days_offset": day_offset,
                "notify_date": notify_date,
                "message": msg
            })

    calculation_details = {
        "price": float(price),
        "t_static": t_static,
        "t_dynamic": t_dynamic,
        "safety_buffer": float(safety_buffer),
        "available_cash": float(available_cash),
        "daily_savings": float(monthly_savings / Decimal(30)) if monthly_savings > 0 else 0,
        "is_banned": is_banned,
        "warning_message": warning_message
    }

    return end_date, final_days, calculation_details, notification_schedule