import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="명절 예매 현황 실시간", layout="centered")

# 1. 구글 시트 연결 설정
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. 기존 데이터 불러오기
df = conn.read(ttl=0) # 실시간 데이터를 위해 캐시(ttl)를 0으로 설정

# --- 관리자 데이터 입력 섹션 ---
PASSWORD = "your_password"
st.sidebar.header("🔐 관리자 모드")
user_pw = st.sidebar.text_input("비밀번호", type="password")

if user_pw == PASSWORD:
    with st.sidebar.form("input_form"):
        st.write("데이터 추가하기")
        new_total = st.text_input("전체 예매율 (%)")
        new_time = st.text_input("시간 (예: 13:00)")
        new_ktx = st.text_input("KTX (%)")
        new_normal = st.text_input("일반 (%)")
        new_itx = st.text_input("ITX (%)")
        
        submit = st.form_submit_button("저장하기")
        
        if submit:
            # 새로운 행 추가 로직
            new_data = pd.DataFrame([{
                "시간": new_time, "KTX": new_ktx, "일반": new_normal, 
                "ITX": new_itx, "전체": new_total
            }])
            updated_df = pd.concat([df, new_data], ignore_index=True)
            conn.update(data=updated_df)
            st.success("데이터가 저장되었습니다!")
            st.rerun()

# --- 메인 보고서 화면 ---
st.title("🚄 실시간 예매 현황 보고")

if not df.empty:
    latest_total = df.iloc[-1]['전체']
    
    # 상단 요약 (가장 최근 전체 예매율)
    st.markdown(f"""
        <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; text-align:center;">
            <h3 style="margin:0; color:#1f77b4;">현재 전체 예매율</h3>
            <h1 style="margin:0; font-size:60px; color:#ff4b4b;">{latest_total}%</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("📋 시간별 상세 현황")
    st.table(df[['시간', 'KTX', '일반', 'ITX']])
else:
    st.info("표시할 데이터가 없습니다.")
