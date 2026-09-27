import requests
import time
import os
import urllib3
import json
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

TOKEN = os.getenv('TOKEN')
API_URL = os.getenv('API').rstrip('/')


def get_chat_id_debug():
    print(f"--- РЕЖИМ ОТЛАДКИ ---")
    print(f"Подключение к: {API_URL}/updates")

    headers = {"Authorization": TOKEN}
    marker = None

    print("Бот запущен. Напишите ему сообщение прямо сейчас...")

    while True:
        params = {"timeout": 10}
        if marker:
            params["marker"] = marker

        try:
            response = requests.get(f"{API_URL}/updates", headers=headers, params=params, verify=False, timeout=20)

            if response.status_code == 200:
                data = response.json()

                # Печатаем ВООБЩЕ ВСЁ, что пришло от сервера
                if data.get("updates") or data.get("result"):
                    print(f"🔔 ПРИШЛО СОБЫТИЕ: {json.dumps(data, indent=2, ensure_ascii=False)}")

                    # Пытаемся автоматически вытащить что-то похожее на ID
                    updates = data.get("updates") or data.get("result") or []
                    for upd in updates:
                        # Запоминаем маркер, чтобы идти дальше
                        marker = upd.get("marker") or upd.get("update_id") or marker
                else:
                    # Если ничего не пришло, просто ставим точку, чтобы видеть, что скрипт жив
                    print(".", end="", flush=True)

            elif response.status_code == 429:
                print("\nToo many requests (429), ждем...")
                time.sleep(5)
            else:
                print(f"\nОшибка {response.status_code}: {response.text}")

        except Exception as e:
            print(f"\nОшибка связи: {e}")
            time.sleep(2)


if __name__ == "__main__":
    get_chat_id_debug()
import requests
import time
import os
import urllib3
import json
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

TOKEN = os.getenv('TOKEN')
API_URL = os.getenv('API').rstrip('/')


def get_chat_id_debug():
    print(f"--- РЕЖИМ ОТЛАДКИ ---")
    print(f"Подключение к: {API_URL}/updates")

    headers = {"Authorization": TOKEN}
    marker = None

    print("Бот запущен. Напишите ему сообщение прямо сейчас...")

    while True:
        params = {"timeout": 10}
        if marker:
            params["marker"] = marker

        try:
            response = requests.get(f"{API_URL}/updates", headers=headers, params=params, verify=False, timeout=20)

            if response.status_code == 200:
                data = response.json()

                # Печатаем ВООБЩЕ ВСЁ, что пришло от сервера
                if data.get("updates") or data.get("result"):
                    print(f"🔔 ПРИШЛО СОБЫТИЕ: {json.dumps(data, indent=2, ensure_ascii=False)}")

                    # Пытаемся автоматически вытащить что-то похожее на ID
                    updates = data.get("updates") or data.get("result") or []
                    for upd in updates:
                        # Запоминаем маркер, чтобы идти дальше
                        marker = upd.get("marker") or upd.get("update_id") or marker
                else:
                    # Если ничего не пришло, просто ставим точку, чтобы видеть, что скрипт жив
                    print(".", end="", flush=True)

            elif response.status_code == 429:
                print("\nToo many requests (429), ждем...")
                time.sleep(5)
            else:
                print(f"\nОшибка {response.status_code}: {response.text}")

        except Exception as e:
            print(f"\nОшибка связи: {e}")
            time.sleep(2)


if __name__ == "__main__":
    get_chat_id_debug()
# from fastapi import FastAPI, HTTPException
# import uvicorn
# from pydantic import BaseModel
# import requests
# import os
# import urllib3
# from dotenv import load_dotenv
#
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# load_dotenv()
#
# TOKEN = os.getenv('TOKEN')
# API_URL = os.getenv('API').rstrip('/')
# ID_DIALOG = os.getenv('ID_DIALOG')
#
# class Base(BaseModel):
#     marka: str
#     name: str
#     vin: str
#     number_phone: str
#
# app = FastAPI()
#
# @app.post('/')
# def create_request(request: Base):
#     text_message = (
#         f"🚗 Новая заявка!\n\n"
#         f"👤 Имя: {request.name}\n"
#         f"🚘 Марка: {request.marka}\n"
#         f"🔢 VIN: {request.vin}\n"
#         f"📞 Телефон: {request.number_phone}"
#     )
#
#     endpoint = f"{API_URL}/messages"
#
#     headers = {
#         "Authorization": TOKEN,
#         "Content-Type": "application/json"
#     }
#
#     # ГЛАВНОЕ ИЗМЕНЕНИЕ: chat_id идет в параметрах URL
#     params = {
#         "chat_id": ID_DIALOG
#     }
#
#     # В теле запроса остается только текст
#     payload = {
#         "text": text_message
#     }
#
#     try:
#         response = requests.post(
#             endpoint,
#             params=params,      # <-- получатель здесь
#             json=payload,       # <-- текст здесь
#             headers=headers,
#             verify=False,
#             timeout=10
#         )
#
#         if response.status_code in [200, 201]:
#             print("✅ Сообщение успешно отправлено в MAX!")
#             return {"status": "success", "info": "Заявка отправлена в MAX"}
#         else:
#             print(f"Ошибка API ({response.status_code}): {response.text}")
#             raise HTTPException(status_code=500, detail=f"Ошибка MAX API: {response.text}")
#
#     except HTTPException:
#         raise
#     except Exception as e:
#         print(f"Ошибка соединения: {e}")
#         raise HTTPException(status_code=500, detail="Ошибка связи с сервером")
#
#
# if __name__ == '__main__':
#     uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)