import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="빅데이터 분석 프로젝트", page_icon="📊")

# 1. 데이터 초기화 (세션 상태에 저장)
if 'df' not in st.session_state:
    data = {
        "이름": ["김철수", "이영희", "박민수", "정수진", "최지훈"],
        "학년": [3, 3, 3, 3, 3],
        "전공": ["컴공", "전자", "수학", "경영", "통계"],
        "Python점수": [85, 92, 78, 95, 88]
    }
    st.session_state.df = pd.DataFrame(data)

# 제목
st.title("빅데이터 분석 프로젝트")
st.write("실시간 데이터 업데이트 예제입니다!")

st.divider()

# 사이드바 설정
st.sidebar.header("새 사용자 추가")
name = st.sidebar.text_input("이름을 입력하세요")
grade = st.sidebar.number_input("학년을 입력하세요", min_value=1, max_value=4, value=1)
major = st.sidebar.text_input("학과를 입력하세요")
score = st.sidebar.number_input("점수를 입력하세요", min_value=0, max_value=100, value=0)

# 버튼을 눌렀을 때만 데이터프레임에 추가
if st.sidebar.button("데이터 추가"):
    new_data = {
        "이름": name,
        "학년": grade,
        "전공": major,
        "Python점수": score
    }
    # 기존 데이터프레임에 새 행 추가
    st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_data])], ignore_index=True)
    # 새로고침 (추가된 내용을 즉시 반영)
    st.rerun()

# 메인 화면 표시 (세션 상태의 데이터를 가져옴)
st.subheader("샘플 데이터")
st.dataframe(st.session_state.df, use_container_width=True)

# 간단한 차트
st.subheader("Python 점수 차트")
st.bar_chart(st.session_state.df.set_index("이름")["Python점수"])