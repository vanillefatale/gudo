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
│   ├── utils/
│   │   └── excel_utils.py            # 엑셀 저장/서식 처리
│   └── run.py                        # 메인 실행 파일
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

## 💾 실행 결과

실행 시 날짜 기준으로 다음과 같은 엑셀 파일이 생성됩니다:

```
📁 20250329_신고신저.xlsx
├── 60일 신고가 (시트)
├── 60일 신저가
├── 250일 신고가
└── 250일 신저가
```

- 전일거래량대비율은 엑셀에서 **% 서식**으로 자동 처리됩니다.
- 불필요한 종목명 (ETN, KOFR, 회사채 등) 필터링 포함
- 등락률 기준 정렬 포함  
  - 신고가: **등락률 내림차순**
  - 신저가: **등락률 내림차순**

---

## 🧩 향후 개발 예정

- [ ] 시가총액 1000억 이상 필터 기능
- [ ] 관련 뉴스 자동 수집 기능
- [ ] 텔레그램 알림 기능
- [ ] 작업 스케줄러(.bat) 등록 통한 자동화

---

## 👨‍💻 Author

- GitHub: [vanillefatale]
- Contact: [vanillefataler@gmail.com]
