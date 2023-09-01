import streamlit as st
import streamlit.components.v1 as components
from streamlit_pills import pills
from streamlit_extras.badges import badge
import openai

st.set_page_config(page_title="Ticket to the Dream - AI B&B", layout="wide", page_icon="⭐️")

@st.cache_data
def load_config():
    config = {
        "openai_api_key": st.secrets["openai_api_key"],
    }
    return config

def mermaid(code):
    components.html(
        f"""
        <pre class="mermaid">
            {code}
        </pre>

        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
        </script>
        """
    , height=350)

### MAIN ###
config = load_config()

openai.api_key = config["openai_api_key"]

gpt_prompt = [{
    "role": "system",
    "content": "You are a chatbot that suggests career path of user input. The user is a student, so you need to respond kindly and easily."
}]

with st.form("prompt-form"):
    st.info("프롬프트 맨 앞에 / 를 붙여 ChatGPT에게 미래를 상상하게 할 수 있습니다!", icon="🤖")
    prompt = st.text_area("Prompt", placeholder="당신의 꿈을 입력해주세요!", key="input")
    submit_prompt = st.form_submit_button("알아보기")

prompt_helper = st.empty()

if submit_prompt and prompt.strip():
    prompt = prompt.strip()

    new_gpt_prompt = gpt_prompt.copy()
    new_gpt_prompt.append({
        "role": "user",
        "content": prompt
    })

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=new_gpt_prompt,
        stream=True)
    
    print(response)

    collected_messages = []
    for chunk in response:
        chunk_message = chunk['choices'][0]['delta']

        if "content" in chunk_message:
            collected_messages.append(chunk_message["content"])
            gpt_response = ''.join(collected_messages)
            prompt_helper.markdown(f"🤖 {gpt_response}")

mermaid("""
timeline
  title 의사가 되기까지의 스텝
  section 중학교
    1. 중학교 졸업 : 중학교 과정을 이수하고 졸업
  section 고등학교
    2. 고등학교 입학 : 고등학교에 입학하고 의학과 관련된 과목에 집중
    3. 대학 준비 : 대학 입시를 위한 준비와 공부
    4. 고등학교 졸업 : 고등학교 과정을 이수하고 졸업
  section 대학교
    5. 의과대학 입학 : 의과대학에 입학
    6. 기초 의학 공부 : 의학의 기초 지식 습득
    7. 임상 실습 : 병원에서의 임상 실습 참여
    8. 의과대학 졸업 : 의과대학 과정을 이수하고 졸업
  section 전문의
    9. 전문의 시험 준비 : 전문의 시험을 위한 공부
    10. 전문의 자격 취득 : 전문의 시험에 합격하고 자격증 취득
""")


import pandas as pd
import random
import plotly.express as px

df = pd.DataFrame(dict(
r=[random.randint(0,2),
    random.randint(0,3),
    random.randint(0,4),
    random.randint(0,5),
    random.randint(0,6)],
theta=['processing cost','mechanical properties','chemical stability',
        'thermal stability', 'device integration']))
fig = px.line_polar(df, r='r', theta='theta', line_close=True)
st.write(fig)