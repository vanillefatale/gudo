import os
import requests
from dotenv import load_dotenv
from highlow.news.summarizer import summarize_news
from highlow.telegram.telegram_notifier import send_telegram_message

# 🔐 환경변수 로딩 (.env)
load_dotenv()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")


def fetch_news(query, display=5):
    """네이버 뉴스 API에서 특정 키워드 관련 뉴스 제목/요약/링크 반환"""
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    params = {
        "query": query,
        "display": display,
        "sort": "date"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"❌ Failed to fetch news for {query}: {response.status_code}")
        return []

    result = []
    for item in response.json().get("items", []):
        title = item["title"].replace("<b>", "").replace("</b>", "")
        desc = item["description"].replace("<b>", "").replace("</b>", "")
        link = item["link"]
        result.append({
            "title": title,
            "description": desc,
            "link": link
        })
    return result


# ✅ 테스트용 실행
if __name__ == "__main__":
    sample_stocks = ["이니텍", "케이피에스", "태경비케이"]

    for name in sample_stocks:
        news_items = fetch_news(name)
        if not news_items:
            print(f"\n📌 [{name}]\n⚠️ 관련 뉴스 없음\n")
            continue

        summary = summarize_news(name, news_items)

        # 메시지 구성
        msg = f"📌 <b>{name}</b>\n📝 <b>상승 이유:</b> {summary}\n\n"
        msg += "<b>🔗 관련 뉴스:</b>\n"
        for item in news_items:
            msg += f"• {item['title']}\n  {item['link']}\n"

        print(msg)
        send_telegram_message(msg)
