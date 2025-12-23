import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="명절 예매 현황 실시간", layout="centered")

# 구글 시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)

# 데이터 불러오기 (ttl=0으로 설정해야 실시간 반영됨)
df = conn.read(ttl=0)

# 관리자 인증
PASSWORD = "your_password" # 여기에 본인만의 비밀번호를 적으세요
st.sidebar.header("🔐 관리자 모드")
user_pw = st.sidebar.text_input("비밀번호", type="password")

if user_pw == PASSWORD:
    with st.sidebar.form("input_form"):
        st.write("📋 문자 데이터 붙여넣기")
        raw_text = st.text_area("형식: 전체예매율\n시간 KTX 일반 ITX", height=200)
        submit = st.form_submit_button("데이터 업데이트")
        
        if submit and raw_text:
            lines = raw_text.strip().split('\n')
            total_val = lines[0].strip() # 첫 줄: 전체 예매율
            
            new_rows = []
            for line in lines[1:]:
                parts = line.split()
                if len(parts) >= 4:
                    new_rows.append({
                        "시간": parts[0], "KTX": parts[1], 
                        "일반": parts[2], "ITX": parts[3], "전체": total_val
                    })
            
            if new_rows:
                # 기존 데이터에 추가 후 저장
                updated_df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
                conn.update(data=updated_df)
                st.sidebar.success("성공적으로 저장되었습니다!")
                st.rerun()

# --- 메인 화면 ---
st.title("🚄 실시간 예매 현황 보고")

if not df.empty:
    # 가장 마지막에 입력된 전체 예매율 가져오기
    latest_total = df.iloc[-1]['전체']
    
    st.markdown(f"""
        <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; text-align:center; border: 2px solid #1f77b4;">
            <h3 style="margin:0; color:#1f77b4;">현재 전체 예매율</h3>
            <h1 style="margin:0; font-size:60px; color:#ff4b4b;">{latest_total}%</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("📋 상세 현황 (누적)")
    # 표 출력 (전체 컬럼 제외하고 시간/KTX/일반/ITX만)
    st.table(df[['시간', 'KTX', '일반', 'ITX']])
else:
    st.info("비밀번호 인증 후 왼쪽에서 데이터를 입력해 주세요.")

