import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="명절 예매 현황 실시간", layout="centered")

# 1. 구글 시트 설정
# 주소 뒤에 /export?format=csv를 붙이면 더 안정적으로 읽어올 수 있습니다.
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-HR4JFkcPC0mJGVFmDS1rcCfgnF0n2z3Env0Ha9d-tQ" 
conn = st.connection("gsheets", type=GSheetsConnection)

# 데이터 로드 (에러 방지 로직 보강)
def load_data():
    try:
        # spreadsheet 인자를 명시적으로 전달
        return conn.read(spreadsheet=SHEET_URL, ttl=0)
    except Exception as e:
        return pd.DataFrame(columns=["시간", "KTX", "일반", "ITX", "전체"])

df = load_data()

# 2. 관리자 인증
PASSWORD = "5485" 
st.sidebar.header("🔐 관리자 모드")
user_pw = st.sidebar.text_input("비밀번호", type="password")

if user_pw == PASSWORD:
    with st.sidebar.form("input_form"):
        st.write("📋 문자 데이터 붙여넣기")
        raw_text = st.text_area("첫줄: 전체예매율 / 다음줄: 시간 KTX 일반 ITX", height=200)
        submit = st.form_submit_button("데이터 서버에 저장")
        
        if submit and raw_text:
            try:
                lines = raw_text.strip().split('\n')
                total_val = lines[0].strip()
                
                new_entries = []
                for line in lines[1:]:
                    parts = line.split()
                    if len(parts) >= 4:
                        new_entries.append({
                            "시간": parts[0], "KTX": parts[1], 
                            "일반": parts[2], "ITX": parts[3], "전체": total_val
                        })
                
                if new_entries:
                    new_df = pd.DataFrame(new_entries)
                    # 데이터 합치기
                    updated_df = pd.concat([df, new_df], ignore_index=True)
                    
                    # [중요] 업데이트 시 spreadsheet 인자를 다시 명시
                    conn.update(spreadsheet=SHEET_URL, data=updated_df)
                    st.sidebar.success("저장 완료!")
                    st.rerun()
            except Exception as e:
                st.sidebar.error(f"저장 중 오류 발생: {e}")

# 3. 메인 화면
st.title("🚄 실시간 예매 현황 보고")

if not df.empty and len(df) > 0:
    # 전체 예매율 표시 (마지막 행)
    latest_total = df.iloc[-1]['전체']
    
    st.markdown(f"""
        <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; text-align:center; border: 2px solid #1f77b4;">
            <p style="margin:0; color:#1f77b4; font-weight:bold;">현재 전체 예매율</p>
            <h1 style="margin:0; font-size:60px; color:#ff4b4b;">{latest_total}%</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("📋 누적 상세 현황")
    st.table(df[['시간', 'KTX', '일반', 'ITX']])
else:
    st.info("데이터가 없습니다. 좌측에서 데이터를 입력해 주세요.")
