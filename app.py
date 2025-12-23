import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="명절 예매 현황 실시간", layout="centered")

# 2. 구글 시트 설정 (성공했던 방식)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-HR4JFkcPC0mJGVFmDS1rcCfgnF0n2z3Env0Ha9d-tQ/edit?usp=drivesdk" # 여기에 성공했던 주소를 그대로 넣으세요
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. 데이터 로드 함수 (에러 방지용)
def load_data():
    try:
        return conn.read(spreadsheet=SHEET_URL, ttl=0)
    except:
        # 시트가 비어있을 경우를 대비해 컬럼명만 있는 표 생성
        return pd.DataFrame(columns=["시간", "KTX", "일반", "ITX", "전체"])

df = load_data()

# 4. 사이드바: 관리자 데이터 입력
PASSWORD = "54850" # 본인만의 비밀번호 설정
st.sidebar.header("🔐 관리자 모드")
user_pw = st.sidebar.text_input("비밀번호", type="password")

if user_pw == PASSWORD:
    with st.sidebar.form("input_form"):
        st.write("📋 문자 데이터 붙여넣기")
        # 예시: 
        # 64.0
        # 13:00 78.7 52.2 15.4
        raw_text = st.text_area("첫줄: 전체예매율 / 다음줄: 시간 KTX 일반 ITX", height=200)
        submit = st.form_submit_button("데이터 서버에 저장")
        
        if submit and raw_text:
            lines = raw_text.strip().split('\n')
            if len(lines) >= 2:
                total_val = lines[0].strip() # 첫 줄은 전체 예매율 숫자만
                
                new_rows = []
                for line in lines[1:]:
                    parts = line.split()
                    if len(parts) >= 4:
                        new_rows.append({
                            "시간": parts[0], "KTX": parts[1], 
                            "일반": parts[2], "ITX": parts[3], "전체": total_val
                        })
                
                if new_rows:
                    # 기존 시트 데이터에 새 데이터 합치기
                    updated_df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
                    # 구글 시트 업데이트
                    conn.update(spreadsheet=SHEET_URL, data=updated_df)
                    st.sidebar.success("서버 저장 완료!")
                    st.rerun()
            else:
                st.sidebar.error("형식이 맞지 않습니다. 첫 줄에 전체 예매율을 적어주세요.")

# 5. 메인 화면 출력
st.title("🚄 실시간 예매 현황 보고")

if not df.empty and len(df) > 0:
    # 가장 마지막에 입력된 전체 예매율을 가져와서 크게 표시
    # '전체' 컬럼의 마지막 값을 가져오기 위해 뒤에서부터 유효한 값을 찾음
    latest_total = df['전체'].iloc[-1]
    
    st.markdown(f"""
        <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; text-align:center; border: 2px solid #1f77b4;">
            <p style="margin:0; color:#1f77b4; font-weight:bold;">현재 전체 예매율</p>
            <h1 style="margin:0; font-size:60px; color:#ff4b4b;">{latest_total}%</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("📋 누적 상세 현황")
    # 화면에는 시간, KTX, 일반, ITX만 깔끔하게 표로 출력
    display_df = df[['시간', 'KTX', '일반', 'ITX']]
    st.table(display_df)
else:
    st.info("비밀번호 입력 후 좌측 사이드바에서 데이터를 입력하면 여기에 표시됩니다.")
