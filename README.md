# Exchange 프로젝트

주식시장 데이터 분석 및 환율 예측 프로젝트

## 📊 데이터 수집

### 수집 기간
- **2020-01-01 ~ 2025-09-30** (약 5년 9개월)

### 수집 지수
| 지수명 | 티커 | 설명 |
|--------|------|------|
| KOSPI | ^KS11 | 한국 종합주가지수 |
| SP500 | ^GSPC | S&P 500 지수 |
| VIX | ^VIX | 변동성 지수 |
| DXY | DX-Y.NYB | 달러 인덱스 |

### 데이터 전처리
- **휴장일 처리**: 이전 거래일 값으로 forward fill
- **2020-01-01 처리**: 2019년 마지막 거래일 값 사용
- **연속 데이터**: 모든 날짜 포함 (휴일/주말 포함)
- **총 데이터 개수**: 약 2,100개 (일별 데이터)

### 저장 위치 data/market_indices_2020_2025_preprocessed.csv

### 컬럼 구조
- `DATE`: 날짜 (2020-01-01 ~ 2025-09-30)
- `KOSPI`: KOSPI 종가
- `SP500`: S&P 500 종가
- `VIX`: VIX 지수
- `DXY`: 달러 인덱스

## 🛠️ 사용 기술
- **Python 3.12**
- **yfinance**: 금융 데이터 수집
- **pandas**: 데이터 전처리

## 📁 프로젝트 구조

## Exchange/
## ├── data/                    # 데이터 저장
## ├── docs/                    # 문서
## ├── models/                  # 모델 저장
## ├── notebooks/               # Jupyter 노트북
## │   └── drawing/
## ├── outputs/                 # 결과물
## └── scripts/                 # 실행 스크립트
## └── market_indices.py    # 데이터 수집 스크립트

## 🚀 실행 방법

### 데이터 수집
```bash
python scripts/market_indices.py
