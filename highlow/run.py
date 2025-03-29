# highlow/run.py

from datetime import datetime
from highlow.kiwoom.kiwoom_fetcher import fetch_high_low_list, clean_kiwoom_data
from highlow.utils.excel_utils import save_multiple_sheets

def get_sorted_df(high_or_low, period):
    """신고가 / 신저가 데이터를 정제 및 등락률 기준으로 정렬"""
    df = fetch_high_low_list(high_or_low, period)
    cleaned = clean_kiwoom_data(df)
    sorted_df = cleaned.sort_values(by="등락률", ascending=False).reset_index(drop=True)
    return sorted_df

if __name__ == "__main__":
    # 📅 오늘 날짜 기준 파일명 생성
    today_str = datetime.now().strftime("%Y%m%d")
    filename = f"{today_str}_신고신저.xlsx"

    # 🧩 데이터 수집
    df_h60 = get_sorted_df("high", "60")
    df_l60 = get_sorted_df("low",  "60")
    df_h250 = get_sorted_df("high", "250")
    df_l250 = get_sorted_df("low",  "250")

    # 📊 시트 구성
    sheet_data = [
        ("60일 신고가", df_h60),
        ("60일 신저가", df_l60),
        ("250일 신고가", df_h250),
        ("250일 신저가", df_l250),
    ]

    # 💾 엑셀 저장
    save_multiple_sheets(sheet_data, filename)
