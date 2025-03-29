# highlow/run_alert.py

from highlow.news.naver_news_fetcher import fetch_news
from highlow.news.summarizer import summarize_news
from highlow.telegram.telegram_notifier import send_telegram_message

def run_news_alert(df):
    """시총 필터링된 종목에 대해 뉴스 요약 및 텔레그램 알림 전송"""
    for _, row in df.iterrows():
        name = row["종목명"]
        news_items = fetch_news(name)
        if not news_items:
            continue

        summary = summarize_news(name, news_items)

        message = f"📌 <b>{name}</b>\n📝 <b>{summary}</b>\n"
        for item in news_items:
            message += f"• {item['title']}\n👉 {item['link']}\n"

        send_telegram_message(message)
