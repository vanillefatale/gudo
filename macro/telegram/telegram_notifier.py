import os
import requests
import time
from dotenv import load_dotenv

# 🔐 .env 로딩
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text, max_retries=3):
    """텔레그램 봇으로 메시지 전송 (rate limit 대응 포함)"""
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

    for attempt in range(1, max_retries + 1):
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ 메시지 전송 완료")
            return
        elif response.status_code == 429:
            data = response.json()
            retry_after = data.get("parameters", {}).get("retry_after", 5)
            print(f"⏳ Rate limit. {retry_after}초 후 재시도... ({attempt}/{max_retries})")
            time.sleep(retry_after + 1)
        else:
            print(f"❌ 전송 실패: {response.status_code}, {response.text}")
            return

    print("❌ 최대 재시도 횟수를 초과했습니다.")
