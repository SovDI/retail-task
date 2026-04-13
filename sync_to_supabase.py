import requests
from supabase import create_client
import json

# --- НАСТРОЙКИ ---
# RetailCRM
RETAIL_URL = "https://diyarsovetkhan.retailcrm.ru/api/v5/orders"
RETAIL_KEY = "fVFCUvcSl4SBX6W8OxEC4crZDkuZEfGh"

# Supabase
# ВНИМАНИЕ: Здесь ОБЯЗАТЕЛЬНО .co на конце
# ОБЯЗАТЕЛЬНО .co на конце! Без буквы 'm'
SUPABASE_URL = "https://fkloidqsfuicnmrwhyri.supabase.co"

# Убедись, что тут нет лишних пробелов или русских букв в начале
SUPABASE_KEY = "sb_secret_YKOE1iUxVzD8CtL85i_bpA_kEDHIZST"

# Telegram
TG_TOKEN = "8729118938:AAHf23roZWmIsZh1zog_Yr1eM1UxSTDVbcI"
CHAT_ID = "521545894"

# Инициализация клиента
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def sync():
    try:
        response = requests.get(RETAIL_URL, params={'apiKey': RETAIL_KEY})
        # Если RetailCRM вернула не 200 OK, мы узнаем об этом здесь
        response.raise_for_status()
        orders = response.json().get('orders', [])
    except Exception as e:
        print(f"❌ Ошибка при запросе к RetailCRM: {e}")
        return

    print(f"📦 Получено {len(orders)} заказов из CRM. Начинаю синхронизацию...")

    for order in orders:
        try:
            total_sum = float(order.get('totalSumm', 0))
            order_num = str(order.get('number', 'unknown'))

            # Шаг 5: Уведомление в Telegram
            if total_sum > 50000:
                msg = f"💰 Крупный заказ #{order_num} на сумму {total_sum} ₸!"
                requests.get(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
                print(f"📢 Уведомление в TG отправлено (#{order_num})")

            # Шаг 3: Сохранение в Supabase
            data = {
                "crm_id": order.get('id'),
                "order_number": order_num,
                "total_sum": total_sum,
                "customer_name": f"{order.get('firstName', '')} {order.get('lastName', '')}".strip()
            }

            # Выполняем upsert (вставка или обновление)
            supabase.table("orders").upsert(data).execute()
            print(f"✅ Заказ {order_num} синхронизирован с Supabase")

        except Exception as e:
            print(f"⚠️ Ошибка при обработке заказа {order.get('number')}: {e}")

if __name__ == "__main__":
    sync()