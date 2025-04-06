# Gudo 프로젝트 🧠📈
> HighLow 종목 수집기와 Macro 자동 리포트 시스템으로 구성된 투자 분석 자동화 툴

```bash
# gudo 폴더에서 실행
python -m highlow.run
python -m macro.run
```

<details>
<summary><strong>📈Gudo HighLow Fetcher 📈</strong></summary>
<br>
키움증권 OpenAPI를 활용한 60일/250일 신고가/신저가 종목 수집기  
자동 엑셀 저장 및 필터링 기능 내장

---

## 📂 디렉토리 구조

```
gudo/
├── highlow/
│   ├── kiwoom/
│   │   └── kiwoom_fetcher.py         # 키움 API 연동 및 데이터 정제
│   │   └── market_cap_filter.py      # 시가총액 1000억 필터링 모듈
│   ├── utils/
│   │   └── excel_utils.py            # 엑셀 저장/서식 처리
│   ├── news/
│   │   └── naver_news_fetcher.py     # 뉴스 제목/요약/링크 수집
│   │   └── summarizer.py             # ChatGPT 요약 API 호출
│   ├── telegram/
│   │   └── telegram_notifier.py      # 텔레그램 메시지 전송
│   └── run.py                        # 메인 실행 파일
│   └── run_alert.py                  # 텔레그램 뉴스 알림 실행 파일
└── README.md
```

---

## 🛠 설치 가이드

### 1️⃣ Python 32bit 설치

> PyKiwoom은 32비트 환경에서만 작동합니다.

- 공식 다운로드: https://www.python.org/downloads/windows/
- 추천 설치 위치:  
  `C:\Python310_32bit`
- 설치 시 옵션:
  - ☑ Add Python to PATH
  - ☑ Install for all users

---

### 2️⃣ 가상환경 및 패키지 설치

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows 기준)
venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

`requirements.txt`에는 다음과 같은 패키지가 포함되어야 합니다:

- pykiwoom  
- pandas  
- openpyxl  

---

### 3️⃣ 키움증권 OpenAPI+ 설치 및 설정

- 설치 링크: https://www.kiwoom.com/h/customer/download/VOpenApiInfoView
- 설치 후 **영웅문4** 실행
- 로그인 시 다음 옵션을 체크:
  - ☑ 고객 아이디 저장
  - ☑ 모의투자 접속 (모의계정이라면)
- 로그인 후 프로그램은 종료하지 말고 **최소화 상태로 유지**

---

## ▶ 실행 방법

```bash
# gudo 폴더에서 실행
python -m highlow.run
```

---


## 🧩 기능별 사용 설명

### 🧾 **Part 1. 신고신저 종목 엑셀 저장기**

**실행 파일**: `highlow/run.py`  
**목적**: 키움 OpenAPI를 활용하여 최근 60일 / 250일 기준 **신고가 / 신저가 종목을 수집**하고, 엑셀 파일로 저장

#### ✅ 주요 특징
- **등락률 기준 정렬**
- **불필요 종목 필터링 (ETN, KOFR, 회사채 등)**
- **엑셀 내 전일거래량대비율은 % 서식 자동 적용**
- **날짜별 엑셀 파일 생성**

#### ▶ 실행 방법

```bash
python -m highlow.run
```

#### 📁 결과물 예시

```
20250329_신고신저.xlsx
├── 60일 신고가
├── 60일 신저가
├── 250일 신고가
└── 250일 신저가
```

---

### 📢 **Part 2. 60일 신고가 뉴스 요약 + 텔레그램 알림**

**실행 파일**: `highlow/run_alert.py`  
**목적**: 60일 신고가 종목 중 **시가총액 1000억 이상 종목**을 필터링하여  
네이버 뉴스 기사 수집 → ChatGPT로 요약 → 텔레그램으로 알림 전송

#### ✅ 주요 흐름

1. 60일 신고가 종목 수집
2. 시가총액 1000억 이상 종목 필터링
3. 네이버 뉴스에서 관련 기사 3~5건 수집 (제목 + 요약 + 링크)
4. ChatGPT를 이용해 핵심 상승 이유 한 줄 요약
5. 텔레그램 채널에 자동 메시지 전송

#### ▶ 실행 방법

```bash
python -m highlow.run_alert
```

#### 💬 텔레그램 메시지 예시

```
📌 [태경비케이]
📝 전남 산불 관련 비료 수요 증가로 주가 상승

• 태경비케이, 비료 관련주로 강세
👉 https://news.naver.com/...

• 전남 산불 확산, 관련 기업 반사이익
👉 https://news.naver.com/...
```

</details>

---

<details>
<summary><strong>📊 Gudo Macro Reporter </strong></summary>
<br>
Finviz 선물지수 차트를 기반으로 주요 자산의 등락 요약을 자동 생성하고  
ChatGPT Vision API를 통해 이유를 분석하여 텔레그램으로 자동 전송하는 매크로 리포터입니다.

---

## 📂 디렉토리 구조

```
gudo/
├── macro/
│   ├── futures/
│   │   ├── macro_futures.py         # Finviz 캡처 및 GPT Vision 분석
│   │   └── screenshots/             # 스크린샷 저장 폴더
│   ├── telegram/
│   │   └── telegram_notifier.py     # 텔레그램 메시지 전송
│   ├── news/
│   │   └── (추후 뉴스 요약 모듈 예정)
│   ├── run.py                       # 메인 실행 파일 (python -m macro.run)
│   └── __init__.py                  # 패키지 인식용
└── README.md
```

---

## 🛠 설치 가이드

### 1️⃣ 필수 설치 패키지

```bash
pip install -r requirements.txt
```

`requirements.txt`에는 다음과 같은 패키지가 포함되어야 합니다:

- openai  
- python-dotenv  
- selenium  
- webdriver-manager  
- yfinance  
- requests  

---

### 2️⃣ .env 파일 구성 예시

```env
OPENAI_API_KEY=sk-xxxxxx
TELEGRAM_BOT_TOKEN=123456:ABCDEF
TELEGRAM_CHAT_ID=987654321
```

※ `.env` 파일은 루트 또는 `macro/` 폴더 안에 위치해야 합니다.

---

## ▶ 실행 방법

```bash
# gudo 폴더에서 실행
python -m macro.run
```

---

## 🔁 자동화 흐름

1. Finviz 선물지수 페이지를 열고 사용자 인증 대기
2. 화면 자동 캡처 후 이미지 저장
3. GPT Vision API를 이용해 이미지 분석 및 요약 생성
4. 주요 상승/하락 자산 및 원인 정리
5. 텔레그램 메시지로 자동 전송

---

## 💬 메시지 예시

```
*MACRO(240406)*

◎ 주요 지표  
S&P500 -1.23%  
Nasdaq -1.42%  
WTI $76.23 (-2.18%)  

◎ 선물 지표  
VIX +23.6%, 시장 불확실성 확대  
USD +0.88%, 안전 자산 수요 증가  
...

◎ 경제 지표 및 발표  
(수동 입력)

◎ 주요 이슈  
(자동 요약 또는 수동 입력)

◎ 종합 정리  
(자동 생성 또는 수동 입력)
```

</details>

---

## 👨‍💻 Author

- GitHub: [vanillefatale]
- Contact: [vanillefataler@gmail.com]
