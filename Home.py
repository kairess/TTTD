import streamlit as st
import streamlit.components.v1 as components
from streamlit_pills import pills
from streamlit_extras.badges import badge
import openai
import pandas as pd
import random
import plotly.express as px
from prompts import *

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
            import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs";
            mermaid.initialize({{ startOnLoad: true, theme: "dark" }});
        </script>
        """
    , height=350)

### MAIN ###
config = load_config()

openai.api_key = config["openai_api_key"]

##### Sidebar #####
with st.sidebar:
    st.header("Ticket to the Dream", divider="rainbow")

    with st.form("parameters-form"):
        st.subheader("사용자 입력")
        job = st.text_input("꿈의 직업")
        name = st.text_input("이름")
        country = st.selectbox("국가", ["한국", "미국", "독일", "베트남"])
        age = st.slider("나이", 10, 30, 15, 1)
        school = st.selectbox("학교", ["초등학교", "중학교", "대학교"])
        mbti = st.selectbox("MBTI", ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP", "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"])
        submit = st.form_submit_button("알아보기")

##### Main #####
answer1 = st.empty()

gpt_prompt = [{
    "role": "system",
    "content": system_prompt
}]

if submit and name and job:
    new_gpt_prompt = gpt_prompt.copy()
    new_user_prompts = user_prompts.copy()

    ### Answer 1 ###
    with st.spinner("꿈으로 향하는 티켓을 발행 중이에요..."):
        new_gpt_prompt.append({
            "role": "user",
            "content": new_user_prompts[0] % (name, country, age, job, school, mbti)
        })

        gpt_response1 = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=new_gpt_prompt,
            stream=True)

        collected_messages = []
        for chunk in gpt_response1:
            chunk_message = chunk["choices"][0]["delta"]
            if "content" in chunk_message:
                collected_messages.append(chunk_message["content"])
                gpt_response1 = "".join(collected_messages)
                answer1.markdown(f"🤖 {gpt_response1}")

        new_gpt_prompt.append({
            "role": "assistant",
            "content": gpt_response1,
        })

    ### Answer 2 ###
    with st.spinner("꿈으로 향하는 로드맵을 그리는 중이에요..."):
        new_gpt_prompt.append({
            "role": "user",
            "content": new_user_prompts[1] % (name, country, age, job, school, mbti),
        })

        gpt_response2 = openai.ChatCompletion.create(
            model="gpt-4",
            messages=new_gpt_prompt,
            stream=False)

        gpt_response2 = gpt_response2["choices"][0]["message"]["content"]
        print(gpt_response2)

        mermaid(gpt_response2)


df = pd.DataFrame(dict(
r=[random.randint(0,2),
    random.randint(0,3),
    random.randint(0,4),
    random.randint(0,5),
    random.randint(0,6)],
theta=["processing cost","mechanical properties","chemical stability",
        "thermal stability", "device integration"]))
fig = px.line_polar(df, r="r", theta="theta", line_close=True)
st.write(fig)