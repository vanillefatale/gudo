from macro.futures.macro_futures import capture_after_manual_auth, analyze_image_with_gpt
from macro.telegram.telegram_notifier import send_telegram_message
from datetime import datetime
import yfinance as yf
import re

# ✅ 텔레그램 MarkdownV2 이스케이프 함수
def escape_markdown_v2(text):
    if not isinstance(text, str):
        text = str(text)
    # 1. 백슬래시 제거
    text = re.sub(r'\\([\\$()*#+\-_.!{}\[\]])', r'\1', text)

    # 2. 강조 기호 제거 (예: **VIX +23.6%** → VIX +23.6%)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)

    # 3. 헤더/번호/해시 제거
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+\.\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[-•]\s*', '', text, flags=re.MULTILINE)

    # 4. 줄 앞뒤 공백 제거
    #text = re.sub(r'^\s+|\s+$', '', text, flags=re.MULTILINE)

    # 5. 자산명 + 변동률 다음의 '-', ':'를 `,`로 바꾸기
    text = re.sub(r'(?<=\d[%])\s*[-:]\s*', ', ', text)
    # 앞뒤 공백 정리
    return text


# ✅ 시장 요약
def fetch_market_summary():
    tickers = {
        "S&P500": "^GSPC",
        "Nasdaq": "^IXIC",
        "WTI": "CL=F"
    }

    results = {}
    for name, ticker in tickers.items():
        data = yf.Ticker(ticker).history(period="2d")
        if len(data) < 2:
            results[name] = "N/A"
            continue

        prev_close = data["Close"].iloc[-2]
        today_close = data["Close"].iloc[-1]
        change_pct = ((today_close - prev_close) / prev_close) * 100

        if name == "WTI":
            results[name] = f"${today_close:.2f} ({change_pct:+.2f}%)"
        else:
            results[name] = f"{change_pct:+.2f}%"

    return results

# ✅ 메시지 생성
def build_macro_message(gpt_summary):
    today = datetime.now().strftime("%y%m%d")
    market = fetch_market_summary()

    msg = f"""*MACRO({today})*\n
◎ 주요 지표  
- S&P500 {market['S&P500']}  
- Nasdaq {market['Nasdaq']}  
- WTI {market['WTI']}  

◎ 선물 지표  
{gpt_summary}

◎ 경제 지표 및 발표  
(수동 입력)

◎ 주요 이슈  
(자동 요약 또는 수동 입력)

◎ 종합 정리  
(자동 생성 또는 수동 입력)
"""
    return msg

# ✅ 실행
if __name__ == "__main__":
    image_path = capture_after_manual_auth()
    gpt_summary = analyze_image_with_gpt(image_path)
    raw_message = build_macro_message(gpt_summary)
    message = escape_markdown_v2(raw_message)
    send_telegram_message(message)
