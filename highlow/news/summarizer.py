import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def summarize_news(stock_name, news_items):
    """
    뉴스 제목 + 요약을 포함해 GPT에게 종목 상승 이유 요약 요청
    """
    combined_news = "\n".join([
        f"- {item['title']} / {item['description']}" for item in news_items
    ])

    prompt = f"""다음은 종목 '{stock_name}'에 대한 최근 뉴스 제목과 요약들이다. 아래 뉴스 중 가장 핵심적인 이유에 집중해서 요약. 이 종목이 상승한 이유를 한 문장으로 간결하게 요약해줘. 기업명 그대로 유지하고, 콤마 넣고 핵심이유 한줄로 뉴스제목처럼 써줘. :

    뉴스 목록: {combined_news}

    요약:"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"❌ 요약 실패: {e}")
        return "요약 실패"
