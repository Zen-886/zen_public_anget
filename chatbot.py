from openai import OpenAI
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    model = st.selectbox(
        "モデルを選択してください",
        ["gpt-4.5-preview", "gpt-4.1-mini", "gpt-4o", "o3", "o3-mini", "o4", "o4-mini"],
        key="chatbot_model"
    )
    "[Refer OpenAI model details](https://platform.openai.com/docs/models)"

st.title("💬 Assistant Bot")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- 入力欄をフォームでラップ（Cmd+Enter送信対応） ---
with st.form(key="chat_form", clear_on_submit=True):
    system_prompt = st.text_area("AIへの指示を入力してください。", value="You are a helpful assistant.", key="system_prompt")
    user_prompt = st.text_area("ユーザーメッセージを入力してください", key="user_prompt")
    submitted = st.form_submit_button("送信 (⌘+Enter で送信)")

if submitted:
    if not openai_api_key:
        st.error("Please add your OpenAI API key to continue.")
        st.stop()
    if not user_prompt:
        st.info("ユーザーメッセージを入力してください。")
        st.stop()

    client = OpenAI(api_key=openai_api_key)

    input_messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "input_text",
                    "text": system_prompt
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": user_prompt
                }
            ]
        }
    ]

    response = client.responses.create(
        model=model,
        input=input_messages,
        text={
            "format": {
                "type": "text"
            }
        },
        reasoning={},
        tools=[],
        temperature=1,
        max_output_tokens=2048,
        top_p=1,
        store=True
    )

    assistant_msg = response.output[0].content[0].text
    st.session_state["messages"].append({"role": "user", "content": user_prompt})
    st.session_state["messages"].append({"role": "assistant", "content": assistant_msg})

# チャット履歴の表示
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])