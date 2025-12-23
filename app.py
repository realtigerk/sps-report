import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="명절 예매 현황 보고", layout="wide")
st.title("🚄 호남선 등 예매 현황 보고")

# 1. 데이터 입력 섹션 (문자 복사 용도)
st.sidebar.header("데이터 입력")
raw_data = st.sidebar.text_area(
    "문자 데이터를 붙여넣으세요", 
    placeholder="예: 09:00 71.4 44.7 10.9\n10:00 74.8 48.1 12.9",
    height=200
)

# 데이터 처리 로직
data_list = []
if raw_data:
    lines = raw_data.strip().split('\n')
    for line in lines:
        parts = line.split()
        if len(parts) >= 4:
            data_list.append({
                "시간": parts[0],
                "KTX": float(parts[1]),
                "일반": float(parts[2]),
                "ITX": float(parts[3])
            })

if data_list:
    df = pd.DataFrame(data_list)
    
    # 2. 상단 요약 정보
    latest = df.iloc[-1]
    col1, col2, col3 = st.columns(3)
    col1.metric("최신 KTX 예매율", f"{latest['KTX']}%")
    col2.metric("일반열차", f"{latest['일반']}%")
    col3.metric("ITX청춘", f"{latest['ITX']}%")

    # 3. 누적 추이 그래프
    st.subheader("📊 시간별 예매율 추이 (누적)")
    st.line_chart(df.set_index("시간"))

    # 4. 상세 데이터 표
    st.subheader("📋 실시간 데이터 현황")
    st.table(df)
else:
    st.info("왼쪽 입력창에 데이터를 입력하면 대시보드가 활성화됩니다.")
