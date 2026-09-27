from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
import requests
import os
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

TOKEN = os.getenv('TOKEN')
API_URL = os.getenv('API').rstrip('/')
ID_DIALOG = os.getenv('ID_DIALOG')


class Base(BaseModel):
    marka: str
    name: str
    vin: str
    number_phone: str


app = FastAPI()


@app.post('/')
def create_request(request: Base):
    # Формируем текст
    text_message = (
        f"🚗 Новая заявка!\n\n"
        f"👤 Имя: {request.name}\n"
        f"🚘 Марка: {request.marka}\n"
        f"🔢 VIN: {request.vin}\n"
        f"📞 Телефон: {request.number_phone}"
    )

    # Адрес для отправки (POST /messages)
    endpoint = f"{API_URL}/messages"

    # Тот самый заголовок, который сработал в тестах
    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "chat_id": ID_DIALOG,
        "text": text_message
    }

    try:
        response = requests.post(endpoint, json=payload, headers=headers, verify=False, timeout=10)

        if response.status_code in [200, 201]:
            return {"status": "success", "info": "Сообщение отправлено в MAX"}
        else:
            print(f"Ошибка API ({response.status_code}): {response.text}")
            raise HTTPException(status_code=500, detail=f"Ошибка MAX API: {response.text}")

    except Exception as e:
        print(f"Ошибка соединения: {e}")
        raise HTTPException(status_code=500, detail="Ошибка связи с сервером")


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)