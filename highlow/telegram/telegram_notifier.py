import os
import requests
from dotenv import load_dotenv

# 🔐 .env 로딩
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text):
    """텔레그램 봇으로 메시지 전송"""
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ TELEGRAM_BOT_TOKEN 또는 CHAT_ID 누락")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }

    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("✅ 메시지 전송 완료")
    else:
        print(f"❌ 전송 실패: {response.status_code}, {response.text}")
