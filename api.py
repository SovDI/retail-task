import requests
import json
import time

# --- ТВОИ ДАННЫЕ ---
BASE_URL = "https://diyarsovetkhan.retailcrm.ru"
API_KEY = "fVFCUvcSl4SBX6W8OxEC4crZDkuZEfGh"
# -------------------

API_ENDPOINT = f"{BASE_URL}/api/v5/orders/create"

def upload_orders(json_file_path):
    try:
        # Читаем файл (убедись, что mock_orders.json лежит в той же папке)
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Ошибка: Файл {json_file_path} не найден в папке со скриптом!")
        return

    # Проверяем структуру: список или объект с ключом orders
    orders = data if isinstance(data, list) else data.get('orders', [])
    print(f"🚀 Найдено заказов: {len(orders)}. Начинаю загрузку в {BASE_URL}...")

    for order in orders:
        payload = {
            'apiKey': API_KEY,
            'order': json.dumps(order)
        }

        try:
            response = requests.post(API_ENDPOINT, data=payload)
            result = response.json()

            if result.get('success'):
                print(f"✅ Заказ #{order.get('number', '???')} успешно создан.")
            else:
                # Если CRM вернула ошибку (например, не хватает обязательного поля)
                print(f"⚠️ Ошибка в заказе {order.get('number')}: {result.get('errors')}")

        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")

        # Пауза, чтобы не превышать лимиты (10 запросов в сек)
        time.sleep(0.1)


if __name__ == "__main__":
    upload_orders('mock_orders.json')