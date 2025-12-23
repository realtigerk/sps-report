import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="명절 예매 현황 보고", layout="centered")

# 1. 구글 시트 연결 (읽기 전용으로 설정)
# 성공하셨던 그 주소를 그대로 넣으세요
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-HR4JFkcPC0mJGVFmDS1rcCfgnF0n2z3Env0Ha9d-tQ/edit?usp=drivesdk" 
conn = st.connection("gsheets", type=GSheetsConnection)

# 캐시 없이 즉시 읽어오기 (ttl=0)
try:
    df = conn.read(spreadsheet=SHEET_URL, ttl=0)
except Exception as e:
    st.error("시트 데이터를 읽어올 수 없습니다. 주소와 권한을 확인해주세요.")
    df = pd.DataFrame()

# 2. 메인 화면 구성
st.title("🚄 실시간 예매 현황 보고")

if not df.empty and len(df) > 0:
    # 가장 마지막 행 데이터 가져오기
    latest_data = df.iloc[-1]
    
    # 상단 요약 대시보드
    st.markdown(f"""
        <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; text-align:center; border: 2px solid #1f77b4;">
            <p style="margin:0; color:#1f77b4; font-weight:bold;">현재 전체 예매율</p>
            <h1 style="margin:0; font-size:60px; color:#ff4b4b;">{latest_data['전체']}%</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # 상세 표 출력
    st.subheader("📋 시간별 상세 현황")
    # 필요한 컬럼만 출력 (시간, KTX, 일반, ITX)
    st.table(df[['시간', 'KTX', '일반', 'ITX']])
    
    st.caption(f"최종 업데이트: {latest_data['시간']} 기준")
else:
    st.info("구글 시트에 데이터를 입력하면 여기에 자동으로 표시됩니다.")
    st.write("시트의 1행이 [시간, KTX, 일반, ITX, 전체] 인지 확인하세요.")
