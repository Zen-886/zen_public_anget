import sys
import os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
import time
from common_utils import export_paired_messages_to_csv

dotenv_path = '.env'
load_dotenv(dotenv_path=dotenv_path)
openai_api_key = os.getenv('OPENAI_API_KEY')


with st.sidebar:
    assistant_id = st.text_input("OpenAI Assistant ID", key="assistant_id", type="password")

st.title("💬 Assistant")

# --- セッション初期化 ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": """How can I help you? Input the "Hi" to understand my function."""}]

if "paired_messages" not in st.session_state:
    st.session_state["paired_messages"] = []

# --- メッセージ履歴表示 ---
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ユーザーからの入力を取得
if msg := st.chat_input():
    if not assistant_id:
        st.info("Please add your Assistant ID to continue.")
        st.stop()

    # OpenAIクライアントを初期化
    client = OpenAI(api_key=openai_api_key)

    # ステップ2: アシスタントを取得 assistant:IT consultant
    my_assistant = client.beta.assistants.retrieve(assistant_id)

    # ステップ3: スレッドを作成
    thread_id = client.beta.threads.create()
    
    # ステップ4: ユーザーのメッセージをスレッドに追加
    user_message = client.beta.threads.messages.create(
        thread_id=thread_id.id,
        role="user",
        content=msg 
    )

    # ステップ5: ユーザーの入力をセッション状態に保存し、画面に表示
    st.session_state.messages.append({"role": "user", "content": msg})
    st.chat_message("user").write(msg)

    
    # ステップ6: アシスタントを実行
  # Execute our run
    # Wait for completion
    def wait_on_run(run, thread_id):
        while run.status != 'completed':
            time.sleep(3)
            run = client.beta.threads.runs.retrieve(run_id=run.id,thread_id=thread_id.id,)

    run = client.beta.threads.runs.create(thread_id=thread_id.id,assistant_id=my_assistant.id,)
    wait_on_run(run, thread_id)

    # Retrieve all the messages added after our last user message
    messages = client.beta.threads.messages.list(
        thread_id=thread_id.id, order="asc", after=user_message.id
    )
    response_message = messages.data[0].content[0].text.value

    # アシスタントの応答をセッション状態に保存し、画面に表示
    st.session_state.messages.append({"role": "assistant", "content":response_message})  # 修正: 正しい内容を保存
    st.chat_message("assistant").write(response_message)  # 修正: 正しい内容を表示

# チャット履歴の初期化や追加はここで
if "paired_messages" not in st.session_state or st.session_state["paired_messages"] is None:
    st.session_state["paired_messages"] = []

def export_sidebar():
    st.header("エクスポート")
    paired_messages = st.session_state.get("paired_messages")
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

# サイドバーで呼び出し
with st.sidebar:
    export_sidebar()