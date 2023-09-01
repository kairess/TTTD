import streamlit as st
from streamlit_pills import pills
from streamlit_extras.badges import badge
import openai

st.set_page_config(page_title="Ticket to the Dream - AI B&B", page_icon="🤖")

@st.cache_data
def load_config():
    config = {
        "openai_api_key": st.secrets["openai_api_key"],
    }
    return config

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

