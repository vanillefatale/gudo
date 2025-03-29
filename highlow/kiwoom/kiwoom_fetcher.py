from pykiwoom.kiwoom import Kiwoom
import pandas as pd

# 전역 객체 생성 (중복 로그인 방지)
kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

def fetch_high_low_list(high_or_low="high", period="60", market="000"):
    print(f"🚀 [{high_or_low}] 종목 수집 시작...", flush=True)

    # API 입력값 설정
    kiwoom.SetInputValue("시장구분", market)
    kiwoom.SetInputValue("고저종구분", "2")
    kiwoom.SetInputValue("종목조건", "0")
    kiwoom.SetInputValue("거래량구분", "00000")
    kiwoom.SetInputValue("신용조건", "0")
    kiwoom.SetInputValue("상하한포함", "1")
    kiwoom.SetInputValue("기간", period)
    kiwoom.SetInputValue("신고저구분", "1" if high_or_low == "high" else "2")

    print("📡 키움 API 호출 중...", flush=True)
    data = kiwoom.block_request("OPT10016", output="신고저가", next=0)
    print("📦 응답 수신 완료", flush=True)

    # DataFrame 처리
    if isinstance(data, pd.DataFrame):
        df = data
    elif isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = pd.DataFrame()

    print(f"✅ [{high_or_low}] 종목 수: {len(df)}", flush=True)
    print("📋 컬럼명:", df.columns.tolist(), flush=True)
    print("🧾 첫 3줄:\n", df.head(3), flush=True)

    return df

def clean_kiwoom_data(df):
    df = df.copy()

    # ✅ 실물 종목 필터링
    keywords = ["ETN", "KOFR", "CD금리", "회사채", "채권", "통안", "레버리지", "인버스"]
    df = df[~df["종목명"].str.contains('|'.join(keywords))].reset_index(drop=True)

    # ✅ 종목코드 포맷 통일
    df["종목코드"] = df["종목코드"].astype(str).str.zfill(6)

    # ✅ 전일대비기호 숫자 → 기호 변환
    sign_map = {"1": "↑", "2": "▲", "3": "↓", "5": "▼"}
    df["전일대비기호"] = df["전일대비기호"].astype(str).map(sign_map)

    # ✅ 전일대비는 숫자만 남기고 부호 제거
    df["전일대비"] = df["전일대비"].astype(str).str.replace("+", "", regex=False).str.replace("-", "", regex=False)
    df["전일대비"] = pd.to_numeric(df["전일대비"], errors="coerce")

    # ✅ 숫자형 컬럼 처리
    numeric_cols = ["현재가", "등락률", "거래량", "전일거래량대비율", "매도호가", "매수호가", "고가", "저가"]
    for col in numeric_cols:
        df[col] = df[col].astype(str).str.replace("+", "", regex=False).str.replace("-", "", regex=False)
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # ✅ 컬럼 순서 재정렬
    ordered_columns = [
        "종목코드", "종목명", "현재가", "전일대비기호", "전일대비", 
        "등락률", "거래량", "전일거래량대비율", "매도호가", "매수호가", "고가", "저가"
    ]
    df = df[[col for col in ordered_columns if col in df.columns]]

    return df