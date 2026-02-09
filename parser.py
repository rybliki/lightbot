import requests
from datetime import datetime

# Твій актуальний графік для черги 2.1
REAL_SCHEDULE = "00:00-00:30, 02:30-08:30, 10:30-16:30, 18:30-24:00"


def get_full_schedule_text():
    n = "\n"  # Створюємо перенос рядка окремо
    return f"📅 **Графік на сьогодні (2.1):**{n}🔴 Відключення:{n}{REAL_SCHEDULE.replace(', ', n)}"



def check_light_status():
    url = "https://voe-poweron.inneti.net/schedule_queues"
    params = {
        "city": "Луцьк",
        "street": "Героїв-Добровольців",
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
        'Referer': 'https://energy.volyn.ua/'
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        if response.status_code == 200:
            now = datetime.now()
            curr_str = now.strftime("%H:%M")
            curr_time = datetime.strptime(curr_str, "%H:%M")

            is_off = False
            next_event = ""
            intervals = REAL_SCHEDULE.split(", ")

            for interval in intervals:
                start_s, end_s = interval.split("-")
                if end_s == "24:00": end_s = "23:59"
                start = datetime.strptime(start_s, "%H:%M")
                end = datetime.strptime(end_s, "%H:%M")

                if start <= curr_time <= end:
                    is_off = True
                    next_event = end_s
                    break

            status_code = "OFF" if is_off else "ON"

            if is_off:
                msg = f"🔴 **Світла НЕМАЄ**\n🕒 Зараз: {curr_str}\n💡 З'явиться о: {next_event}"
            else:
                next_event = ""
                for interval in intervals:
                    start_s, _ = interval.split("-")
                    if start_s > curr_str:
                        next_event = start_s
                        break
                msg = f"🟢 **Світло Є**\n🕒 Зараз: {curr_str}"
                if next_event:
                    msg += f"\n⚠️ Відключення о: {next_event}"

            return msg, status_code, next_event
        return "⚠️ Помилка сервера обленерго", "ERROR", ""
    except Exception as e:
        return f"❌ Помилка зв'язку: {str(e)}", "ERROR", ""
