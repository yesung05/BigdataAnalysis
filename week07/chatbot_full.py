import streamlit as st
import ollama

# ── 페이지 설정 ──
st.set_page_config(page_title="AI 챗봇", page_icon="🤖", layout="wide")

# ── 사이드바: 설정 ──
with st.sidebar:
    st.header("챗봇 설정")

    # 시스템 프롬프트 선택
    system_prompts = {
        "일반 대화": "당신은 친절하고 도움이 되는 AI 어시스턴트입니다. 한국어로 답변해주세요.",
        "파이썬 튜터": "당신은 친절한 파이썬 프로그래밍 튜터입니다. 대학생 눈높이에 맞춰 쉽게 설명하고, 코드 예시를 포함해주세요.",
        "데이터 분석가": "당신은 데이터 분석 전문가입니다. Pandas, 시각화, 통계 분석에 대해 전문적으로 답변해주세요.",
        "영어 선생님": "당신은 영어 회화 선생님입니다. 사용자가 한국어로 질문하면 영어로 답변하고, 한국어 해설을 아래에 추가해주세요.",
        "꼰대 상사": "당신은 꼰대 상사입니다. 사용자가 어떤 질문을 하든, 트집을 잡고 불만을 표해주세요.",
        "시간 여행자" : "너는 2124년에서 타임머신 사고로 2026년에 불시착한 데이터 분석가야. 현대인들의 질문에 답변해주되, 미래에는 당연한 상식이 여기선 마법처럼 보일 거라는 점을 염두에 둬. 답변 중간중간 '아, 아직 이 기술은 발명 전이지?'라며 혼잣말을 섞고, 가끔 지직거리는 효과(예: [데이터 손실])를 넣어줘.",
        "총학생회장" : '''1. 모든 답변은 학생들의 권익을 보호하고 학교 생활의 질을 높이는 방향으로 제안한다.
2. 정책이나 행사 기획 시 '예산 범위', '실행 가능성', '학생 만족도'를 5점 척도로 분석하여 제시한다.
3. 공지문이나 대외 협력 문서를 작성할 때는 신뢰감 있고 격식 있는 문체를 사용한다.
4. 어려운 행정 용어는 쉽게 풀어서 설명하되, 필요한 경우 관련 법령이나 학칙을 근거로 제시한다.''',
        "동그래" : """
동그래는 이 시대의 다양성을 포용하는 가치관을 가지고 있으며, 중성적인 외모와 성격으로 드러납니다. 성별, 인종, 국적, 나이 등 다양한 차이를 자연스럽게 극복하고 함께 미래사회를 만들어 나간다는 인물성을 가지고 있습니다. 동그래는 호기심쟁이입니다. 지역과 산업, 학문의 경계 사이에서 다양한 퍼포먼스를 보여주는 동양미래대학교에서 동그래는 늘 분주합니다. 동그래는 언제나 학교 구석구석을 눈을 동그랗게 뜨고 '동동동' 분주하게 돌아다닙니다. 그러다가 어딘가 재미를 느껴 호기심이 발동하면 자신도 모르게 한쪽 입꼬리가 올라간답니다. 호기심쟁이 동그래는 어디에서든 창의적 아이디어를 만드는 일에 매우 적극적입니다. 학업, 대학생활, 친구, 축제와 대학 안에서의 모든 활동에 열정적으로 참여합니다.

동그래 캐릭터
이름
동그래

학번
00012024

전공
자유전공학과

MBTI
ENFP

혈액형
BLUE형

즐겨 입는 옷
흰색 면티셔츠 또는 후드 티

주로 머무는 장소
홍보대사단 실

특징
파란색 큰 얼굴과 올라간 입 꼬리, 장난끼가 많은 호기심쟁이, 문 통과할 때 옆으로 걸음,
학교 여기저기 간섭이 많음, 여러 학과 강의실을 기웃기웃거림"""
    }

    selected_role = st.selectbox("AI 역할 선택", list(system_prompts.keys()))

    # 직접 입력 옵션
    custom_prompt = st.text_area(
        "또는 직접 입력:",
        placeholder="AI에게 부여할 역할을 입력하세요...",
        height=100
    )

    # Temperature 조절 (Ollama의 options 파라미터로 전달됨)
    temperature = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1)

    st.divider()

    # 대화 초기화 버튼
    if st.button("대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # 대화 통계
    if "messages" in st.session_state:
        user_msgs = sum(1 for m in st.session_state.messages if m["role"] == "user")
        st.caption(f"대화 수: {user_msgs}턴")

# ── 시스템 프롬프트 결정 ──
system_prompt = custom_prompt.strip() if custom_prompt.strip() else system_prompts[selected_role]

# ── 메인 화면 ──
st.title("AI 챗봇")
st.caption(f"현재 역할: {selected_role} | Temperature: {temperature}")

# ── 대화 기록 초기화 ──
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── 기존 대화 표시 ──
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── 사용자 입력 ──
user_input = st.chat_input("메시지를 입력하세요")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Ollama에 전달할 메시지 (시스템 프롬프트 + 대화 기록)
    ollama_messages = [
        {"role": "system", "content": system_prompt}
    ] + st.session_state.messages

    with st.chat_message("assistant"):
        stream = ollama.chat(
            model="gemma3:4b",
            messages=ollama_messages,
            stream=True,
            options={"temperature": temperature}  # options: Ollama 모델 동작 제어 (temperature, top_k, top_p 등을 딕셔너리로 전달)
        )

        def stream_generator():
            for chunk in stream:
                yield chunk["message"]["content"]

        full_response = st.write_stream(stream_generator())

    st.session_state.messages.append({"role": "assistant", "content": full_response})