import os
import time
import base64
import openai
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# 🔐 .env 로딩
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ 1. 날짜 기반 파일명을 자동으로 생성하고 캡처
def capture_after_manual_auth():
    today_str = datetime.now().strftime("%Y%m%d")
    screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    save_path = os.path.join(screenshot_dir, f"finviz_futures_{today_str}.png")

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://finviz.com/futures_performance.ashx")

    waiting_time = 1
    print("\n🔒 사람이 인증을 직접 완료해주세요.")
    print(f"✅ 인증 완료 후 {waiting_time}초 뒤 자동으로 캡처됩니다.\n")

    for i in range(waiting_time, 0, -1):
        print(f"⏳ 인증 대기 중... {i}초 남음", end="\r")
        time.sleep(1)

    time.sleep(5)
    driver.save_screenshot(save_path)
    print(f"\n📸 스크린샷 저장 완료: {save_path}")

    driver.quit()
    return save_path

# ✅ 2. 이미지 base64 인코딩
def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ✅ 3. GPT Vision 분석
def analyze_image_with_gpt(image_path):
    image_base64 = image_to_base64(image_path)

    print("🔍 GPT Vision에 이미지 전송 중...")

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "이 이미지에서 Top 5 상승 및 하락 자산을 각각 퍼센트와 함께 요약해줘. "
                            "각 자산에 대해 왜 그렇게 움직였는지 시장 뉴스 기반으로 간단히 추정해줘. "
                            "출력 포맷:\n"
                            "코코아 +3.24%, 서아프리카 지역 기상 악화와 물류 지연으로 공급 차질 지속"
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image_base64}"}
                    }
                ]
            }
        ],
        max_tokens=1000
    )

    return response["choices"][0]["message"]["content"]
