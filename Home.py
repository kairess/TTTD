import streamlit as st
import streamlit.components.v1 as components
import openai
import pandas as pd
import json
import plotly.express as px
from prompts import *

is_answer = [True, True, True, True]

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
    , height=500)

config = load_config()
openai.api_key = config["openai_api_key"]

### MAIN ###
st.header("Ticket to the Dream", divider='rainbow')

with st.expander("서비스 소개", expanded=True):
    st.write("""Ticket to the Dream 서비스는 당신의 꿈의 이루기 위해 안내를 주는 도우미입니다.\n\n왼쪽 사이드바에 여러분의 정보를 입력해주세요.""")

##### Sidebar #####
with st.sidebar:
    st.header("Ticket to the Dream", divider="rainbow")

    with st.form("parameters-form"):
        st.subheader("사용자 입력")
        job = st.text_input("꿈의 직업")
        name = st.text_input("이름")
        country = st.selectbox("국가", ["한국", "미국", "독일", "베트남"])
        age = st.slider("나이", 10, 40, 15, 1)
        school = st.selectbox("학교", ["초등학교", "중학교", "고등학교", "대학교", "대학원"], index=1)
        mbti = st.selectbox("MBTI", ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP", "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"])
        submit = st.form_submit_button("알아보기")

##### Main #####
gpt_prompt = [{
    "role": "system",
    "content": system_prompt
}]

if submit and name and job:
    new_gpt_prompt = gpt_prompt.copy()
    new_user_prompts = user_prompts.copy()

    ### Answer 1 ###
    if is_answer[0]:
        st.subheader(f"{name}님의 꿈을 향한 티켓", divider=True)
        answer1 = st.empty()

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
    if is_answer[1]:
        st.subheader(f"{name}님의 꿈으로 향하는 로드맵", divider=True)
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

            start_keyword = "```mermaid"
            end_keyword = "```"

            if start_keyword in gpt_response2 and end_keyword in gpt_response2:
                mermaid_start = gpt_response2.find(start_keyword) + len(start_keyword)
                mermaid_end = gpt_response2.find(end_keyword, mermaid_start)
                mermaid_content = gpt_response2[mermaid_start:mermaid_end].strip()
            else:
                st.markdown(f"No mermaid content found!\n\n```{gpt_response2}```")

            mermaid(mermaid_content)

            # new_gpt_prompt.append({
            #     "role": "assistant",
            #     "content": gpt_response2,
            # })

    ### Answer 3 ###
    if is_answer[2]:
        st.subheader(f"AI가 분석한 {job}", divider=True)
        with st.spinner("꿈으로 향하는 능력치를 계산하는 중이에요..."):
            new_gpt_prompt.append({
                "role": "user",
                "content": new_user_prompts[2],
            })

            gpt_response3 = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=new_gpt_prompt,
                stream=False)

            gpt_response3 = gpt_response3["choices"][0]["message"]["content"]

            start_keyword = "{"
            end_keyword = "}"

            if start_keyword in gpt_response3 and end_keyword in gpt_response3:
                list_start = gpt_response3.find(start_keyword) + len(start_keyword)
                list_end = gpt_response3.find(end_keyword, list_start)
                list_content = gpt_response3[list_start-1:list_end+1].strip()
            else:
                st.markdown(f"No Python List content found!\n\n```{gpt_response3}```")

            print(list_content)

            list_content = json.loads(list_content)

            df = pd.DataFrame(dict(
                r=list_content["score"],
                theta=["직업적합도", "난이도", "소요비용", "소요기간", "예상수입", "업무강도"]))
            fig = px.line_polar(df, r="r", theta="theta", line_close=True)
            fig.update_traces(fill="toself")
            st.write(fig)
            st.markdown(list_content["description"])

    ### Answer 4 ###
    if is_answer[3]:
        st.subheader(f"AI가 그린 {name}님의 미래 모습", divider=True)
        with st.spinner("미래의 당신을 그리는 중이에요..."):
            gpt_prompt_dalle = [{
                "role": "system",
                "content": dalle_prompt_ori
            },
            {
                "role": "user",
                "content": job,
            }]

            gpt_response4 = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=gpt_prompt_dalle,
                stream=False)

            gpt_response4 = gpt_response4["choices"][0]["message"]["content"].replace("Output:", "").strip()

            print(gpt_response4)

            dalle_response = openai.Image.create(
                prompt=f"a portrait of {gpt_response4}, cheering and friendly mood, cartoon low poly style.",
                n=1,
                size="512x512"
            )
            image_url = dalle_response['data'][0]['url']
            st.image(image_url)

    st.button("친구에게 공유하기")
