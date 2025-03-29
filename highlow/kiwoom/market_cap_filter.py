from pykiwoom.kiwoom import Kiwoom
import pandas as pd
import time

# 전역 객체 (중복 로그인 방지)
kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

# ✅ 종목별 시가총액 조회
def get_market_cap(code):
    kiwoom.SetInputValue("종목코드", code)
    data = kiwoom.block_request("OPT10001", output="주식기본정보", next=0)
    raw = data.get("시가총액", "0")
    try:
        return int(raw.replace(",", ""))
    except:
        return None

# ✅ 시가총액 컬럼 추가 (with sleep + 로그)
def add_market_cap_column(df):
    df = df.copy()
    market_caps = []

    for idx, code in enumerate(df["종목코드"]):
        cap = get_market_cap(code)
        market_caps.append(cap)
        print(f"🔍 ({idx+1}/{len(df)}) {code} → {cap}")
        time.sleep(0.5)  # 키움 요청 간 딜레이

    df["시가총액"] = market_caps
    return df

# ✅ 시총 기준 필터링
def filter_by_market_cap(df, threshold=1000):  # 1000억
    df = add_market_cap_column(df)
    return df[df["시가총액"] >= threshold].reset_index(drop=True)
