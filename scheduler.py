import asyncio
from parser import check_light_status
from database import get_all_users
from datetime import datetime


async def schedule_checker(bot):
    last_status_code = ""
    reminded_event = ""
    print("⏰ Планувальник запущено (перевірка кожні 15 хв)")

    while True:
        try:
            current_msg, status_code, next_event_time = check_light_status()
            users = get_all_users()

            # 1. Якщо статус змінився (наприклад, дали світло)
            if status_code != last_status_code and status_code != "ERROR":
                for user_id in users:
                    try:
                        await bot.send_message(user_id, f"🔔 **ОНОВЛЕННЯ СТАТУСУ:**\n\n{current_msg}")
                    except:
                        pass
                last_status_code = status_code

            # 2. Нагадування за 15 хв до вимкнення
            if status_code == "ON" and next_event_time:
                now = datetime.now()
                # Розраховуємо різницю в часі
                event_h, event_m = map(int, next_event_time.split(":"))
                event_dt = now.replace(hour=event_h, minute=event_m, second=0)

                diff = (event_dt - now).total_seconds() / 60
                if 10 <= diff <= 16 and reminded_event != next_event_time:
                    for user_id in users:
                        try:
                            await bot.send_message(user_id,
                                                   f"⚠️ **УВАГА!** Світло вимкнуть приблизно за 15 хвилин (о {next_event_time})!")
                        except:
                            pass
                    reminded_event = next_event_time

            await asyncio.sleep(900)  # 15 хвилин
        except Exception as e:
            print(f"Помилка планувальника: {e}")
            await asyncio.sleep(60)