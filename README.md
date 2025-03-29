# Gudo HighLow Fetcher 📈

키움증권 OpenAPI를 활용한 60일/250일 신고가/신저가 종목 수집기  
자동 엑셀 저장 및 필터링 기능 내장

## 📂 구성
- `highlow/kiwoom/kiwoom_fetcher.py`: 키움 API 연동 및 데이터 정제
- `highlow/utils/excel_utils.py`: 엑셀 저장/서식 처리
- `highlow/run.py`: 메인 실행 파일

## 🛠 설치
```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

## ▶ 실행 (gudo 위치에서 명령어 수행)
```bash
python -m highlow.run
```