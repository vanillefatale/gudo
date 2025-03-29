# Gudo HighLow Fetcher 📈

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

---

## 👨‍💻 Author

- GitHub: [vanillefatale]
- Contact: [vanillefataler@gmail.com]
