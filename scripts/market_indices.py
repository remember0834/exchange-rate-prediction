"""
주식시장 지수 데이터 수집 및 전처리 (1월 1일 포함)
VS Code 실행용
"""

import yfinance as yf
import pandas as pd
import os

print("=" * 60)
print("주식시장 지수 데이터 수집")
print("=" * 60)

# 기간 설정 (2019년 12월부터 시작하여 전날 데이터 확보)
START_DATE = "2019-12-01"
END_DATE = "2025-10-05"

# 수집할 지수
INDICES = {
    'KOSPI': '^KS11',
    'SP500': '^GSPC',
    'VIX': '^VIX',
    'DXY': 'DX-Y.NYB'
}

# 데이터 수집
ALL_DATA = []

for NAME, TICKER in INDICES.items():
    print(f"\n{NAME} 수집 중... (티커: {TICKER})")
    
    try:
        DATA = yf.download(TICKER, start=START_DATE, end=END_DATE, 
                          progress=False, auto_adjust=True)
        
        if not DATA.empty:
            DF = DATA[['Close']].reset_index()
            DF.columns = ['DATE', NAME]
            ALL_DATA.append(DF)
            
            print(f"✓ {len(DF)}개 수집 완료")
            print(f"  기간: {DF['DATE'].min().date()} ~ {DF['DATE'].max().date()}")
    except Exception as E:
        print(f"✗ 오류: {E}")

# 데이터 통합 및 전처리
if ALL_DATA:
    print("\n" + "=" * 60)
    print("데이터 통합 및 전처리")
    print("=" * 60)
    
    # 1. 날짜 기준 병합
    MERGED = ALL_DATA[0]
    for DF in ALL_DATA[1:]:
        MERGED = MERGED.merge(DF, on='DATE', how='outer')
    
    # 2. 날짜 순 정렬
    MERGED = MERGED.sort_values('DATE').reset_index(drop=True)
    MERGED['DATE'] = pd.to_datetime(MERGED['DATE'])
    
    # 3. 전체 날짜 범위 생성 (2020-01-01 ~ 2025-09-30)
    DATE_RANGE = pd.date_range(start='2020-01-01', end='2025-09-30', freq='D')
    FULL_DF = pd.DataFrame({'DATE': DATE_RANGE})
    
    # 4. 기존 데이터와 병합
    MERGED_FILLED = FULL_DF.merge(MERGED, on='DATE', how='left')
    
    # 5. Forward fill (휴장일은 이전 거래일 값 사용)
    MERGED_FILLED = MERGED_FILLED.fillna(method='ffill')
    
    # 6. 2020-01-01이 아직 NaN이면 이전 데이터로 채우기
    if MERGED_FILLED.loc[0].isnull().any():
        # 2019년 마지막 거래일 값 찾기
        LAST_2019 = MERGED[MERGED['DATE'] < '2020-01-01'].tail(1)
        if not LAST_2019.empty:
            for COL in ['KOSPI', 'SP500', 'VIX', 'DXY']:
                if pd.isna(MERGED_FILLED.loc[0, COL]):
                    MERGED_FILLED.loc[0, COL] = LAST_2019[COL].values[0]
    
    # 7. 남은 결측치 처리 (backward fill)
    MERGED_FILLED = MERGED_FILLED.fillna(method='bfill')
    
    print("\n결측치 확인:")
    print(MERGED_FILLED.isnull().sum())
    
    # 8. 최종 결과 확인
    print("\n" + "=" * 60)
    print("전처리 완료")
    print("=" * 60)
    print(f"최종 기간: {MERGED_FILLED['DATE'].min().date()} ~ {MERGED_FILLED['DATE'].max().date()}")
    print(f"총 데이터: {len(MERGED_FILLED):,}개")
    
    # 9. 2020년 1월 초 데이터 확인
    print("\n2020년 1월 첫 10일:")
    JAN_2020 = MERGED_FILLED[
        (MERGED_FILLED['DATE'].dt.year == 2020) & 
        (MERGED_FILLED['DATE'].dt.month == 1)
    ].head(10)
    print(JAN_2020)
    
    # 10. 2019년 마지막 거래일 확인 (참고용)
    print("\n2019년 마지막 거래일 (참고):")
    LAST_2019_TRADING = MERGED[MERGED['DATE'] < '2020-01-01'].tail(1)
    print(LAST_2019_TRADING)
    
    # 11. outputs 폴더에 CSV 저장
    data_DIR = "data"
    os.makedirs(data_DIR, exist_ok=True)  # 폴더가 없으면 생성
    
    OUTPUT_FILE = os.path.join(data_DIR, "market_indices_2020_2025_preprocessed.csv")
    MERGED_FILLED.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    
    # 저장 경로 출력
    FULL_PATH = os.path.abspath(OUTPUT_FILE)
    print(f"\n✓ 저장 완료: {OUTPUT_FILE}")
    print(f"  전체 경로: {FULL_PATH}")
    
    # 12. 기초 통계
    print("\n기초 통계:")
    print(MERGED_FILLED[['KOSPI', 'SP500', 'VIX', 'DXY']].describe())
    
else:
    print("\n수집된 데이터가 없습니다.")

print("\n" + "=" * 60)
print("완료!")
print("=" * 60)