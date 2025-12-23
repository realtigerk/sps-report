import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="명절 예매 현황", layout="centered")

# 제목
st.title("🚄 호남선 등 예매 현황 보고")

# 1. 사이드바 입력창
st.sidebar.header("📊 데이터 입력")
st.sidebar.info("입력 예시:\n64.0\n09:00 71.4 44.7 10.9\n10:00 74.8 48.1 12.9")

raw_input = st.sidebar.text_area(
    "데이터를 붙여넣으세요 (첫 줄은 전체 예매율)",
    height=300
)

if raw_input:
    lines = raw_input.strip().split('\n')
    
    # 첫 번째 줄: 전체 예매율
    total_rate = lines[0].strip()
    
    # 두 번째 줄부터: 시간별 상세 데이터
    details = []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) >= 4:
            details.append({
                "시간": parts[0],
                "KTX (%)": parts[1],
                "일반 (%)": parts[2],
                "ITX (%)": parts[3]
            })

    # 2. 메인 화면 - 전체 예매율 크게 표시
    st.markdown(f"""
        <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; text-align:center;">
            <h3 style="margin:0; color:#1f77b4;">현재 전체 예매율</h3>
            <h1 style="margin:0; font-size:60px; color:#ff4b4b;">{total_rate}%</h1>
        </div>
    """, unsafe_allow_html=True)

    st.write("---")

    # 3. 상세 데이터 표 표시
    if details:
        st.subheader("📋 시간별/열차종별 상세 현황")
        df = pd.DataFrame(details)
        # 표를 화면 꽉 차게 표시
        st.table(df)
    else:
        st.warning("시간별 데이터를 입력해 주세요.")
else:
    st.info("왼쪽 사이드바에 데이터를 입력하면 보고서가 생성됩니다.")
