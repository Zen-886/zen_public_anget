import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
import time
from common_utils import export_paired_messages_to_csv

st.title("💬 Assistant")
# --- セッション初期化 ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "OpenaiのAPIキーとアシスタントIDを入力してください。"}]
if "paired_messages" not in st.session_state:
    st.session_state["paired_messages"] = []

# --- サイドバー ---
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    assistant_id = st.text_input("OpenAI Assistant ID", key="assistant_id", type="password")
    st.header("履歴エクスポート")
    # ここで毎回最新のセッションステートを参照
    paired_messages = st.session_state.get("paired_messages", [])
    if isinstance(paired_messages, list) and len(paired_messages) > 0:
        csv_data = export_paired_messages_to_csv(paired_messages)
        st.download_button(
            label="💾 チャット履歴をCSVダウンロード",
            data=csv_data.encode('utf-8-sig'),
            file_name="chat_history.csv",
            mime="text/csv"
        )
    else:
        st.info("チャット履歴がありません。")

# --- メッセージ履歴表示 ---
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- チャット入力 ---
# ユーザーからの入力を取得（Cmd+Enter送信対応）
with st.form(key="chat_form", clear_on_submit=True):
    msg = st.text_area("メッセージを入力してください", key="user_input", height=80)
    submitted = st.form_submit_button("送信 (⌘+Enter で送信)")

if submitted and msg:
    if not openai_api_key:
        st.info("Please confirm your OpenAI API key to continue.")
        st.stop()
    if not assistant_id:
        st.info("Please add your Assistant ID to continue.")
        st.stop()

    try:
        client = OpenAI(api_key=openai_api_key)
        my_assistant = client.beta.assistants.retrieve(assistant_id)

        # スレッドIDがあればそれを使い、なければ新規作成
        if st.session_state.get("thread_id"):
            thread_id = type("Thread", (), {"id": st.session_state["thread_id"]})()
            # 送信前にアクティブrunがあればキャンセル
            runs = client.beta.threads.runs.list(thread_id=thread_id.id)
            for run in runs.data:
                if run.status not in ["completed", "cancelled", "failed", "expired"]:
                    try:
                        client.beta.threads.runs.cancel(thread_id=thread_id.id, run_id=run.id)
                    except Exception as e:
                        st.warning(f"既存のアクティブrunのキャンセルに失敗: {e}")
        else:
            thread_id = client.beta.threads.create()
            st.session_state["thread_id"] = thread_id.id

        user_message = client.beta.threads.messages.create(
            thread_id=thread_id.id,
            role="user",
            content=msg 
        )
        st.session_state.messages.append({"role": "user", "content": msg})
        st.chat_message("user").write(msg)

        def wait_on_run(run, thread_id):
            while run.status != 'completed':
                time.sleep(3)
                run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=thread_id.id)

        run = client.beta.threads.runs.create(thread_id=thread_id.id, assistant_id=my_assistant.id)
        wait_on_run(run, thread_id)

        messages = client.beta.threads.messages.list(
            thread_id=thread_id.id, order="asc", after=user_message.id
        )

        run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id.id, run_id=run.id)
        step_usage = {"total_tokens": "", "completion_tokens": "", "prompt_tokens": ""}
        for run_step in run_steps.data:
            if hasattr(run_step.step_details, "message_creation"):
                message_id = getattr(run_step.step_details.message_creation, "message_id", None)
                if message_id == messages.data[0].id:
                    usage = getattr(run_step, "usage", None)
                    if usage:
                        step_usage = {
                            "total_tokens": getattr(usage, "total_tokens", ""),
                            "completion_tokens": getattr(usage, "completion_tokens", ""),
                            "prompt_tokens": getattr(usage, "prompt_tokens", "")
                        }
                    break

        response_message = messages.data[0].content[0].text.value

        st.session_state.messages.append({"role": "assistant", "content": response_message})
        st.chat_message("assistant").write(response_message)

        created_at = getattr(messages.data[0], "created_at", "")
        if created_at:
            try:
                created_at = datetime.fromtimestamp(created_at).strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                pass
        assistant_id_val = getattr(my_assistant, "id", "")

        st.session_state["paired_messages"].append({
            "assistant_id": assistant_id_val,
            "thread_id": thread_id.id,
            "created_at": created_at,
            "user_input": msg,
            "output": response_message,
            "Total_Tokens": step_usage["total_tokens"],
            "Completion_Tokens": step_usage["completion_tokens"],
            "Prompt_Tokens": step_usage["prompt_tokens"]
        })

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")