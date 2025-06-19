# Zen_public_agent

## 概要
Zen_public_agentは、OpenAI APIとStreamlitを活用したチャットボットWebアプリです。  
ユーザーはOpenAIのAPIキーを入力し、複数のモデルを選択して対話できます。

## 特徴
- StreamlitによるシンプルなWebチャットUI
- OpenAIの各種モデル（gpt-4.5-preview, gpt-4o等）に対応
- .envによるAPIキー管理（APIキーは絶対に公開しないでください）
- Docker/DevContainer対応
- チャット履歴のCSVエクスポート機能（拡張ページあり）

## セットアップ

### 1. 必要条件
- Python 3.11 以上
- pip
- OpenAI APIキー（[取得はこちら](https://platform.openai.com/account/api-keys)）

### 2. クローン & インストール

```bash
git clone https://github.com/your-username/Zen_public_agent.git
cd Zen_public_agent
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. .envファイルの作成

`.env` ファイルをプロジェクトルートに作成し、以下のように記載してください。  
**スペースやクォートは不要です。**

```
OPENAI_API_KEY=your_openai_api_key_here
```

※ `.env` は `.gitignore` に追加し、絶対に公開リポジトリに含めないでください。

### 4. 起動方法

```bash
streamlit run chatbot.py
```

または、拡張機能ページを利用する場合は `pages/` ディレクトリ内のファイルを指定してください。

---

## 主要ファイル

- `chatbot.py` … メインのチャットボットアプリ
- `requirements.txt` … 必要なPythonパッケージ
- `pages/` … 拡張機能（下記参照）
- `.devcontainer/Dockerfile` … DevContainer用Dockerfile
- `common_utils.py` … チャット履歴エクスポート用ユーティリティ

### `pages/`ディレクトリの主なファイル
- `A_set_assistant_id.py` … アシスタントIDを指定してチャット
- `A_set_api_key_assistant_id.py` … APIキーとアシスタントIDを指定してチャット
- `B_export_history.py` … チャット履歴のCSVエクスポート

---

## チャット履歴エクスポート機能

`B_export_history.py`ページで、これまでのチャット履歴をCSV形式でダウンロードできます。  
出力内容には、ユーザー・アシスタントの発言やタイムスタンプなどが含まれます。

---

## セキュリティ・注意事項

- **APIキーやアシスタントIDは絶対に公開しないでください。**  
  `.env`ファイルや個人情報を含むファイルは、`.gitignore`に追加し、リポジトリに含めないようにしてください。
- OpenAI API利用には従量課金が発生します。APIキーの管理・利用には十分ご注意ください。
- 悪意ある入力（プロンプトインジェクション等）への対策は難しいですが、必要に応じて入力内容のフィルタリングや長さ制限を検討してください。

---

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。  
詳細は`LICENSE`ファイルをご確認ください。

---

## 参考リンク

- [Streamlit公式ドキュメント](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps)
- [OpenAI APIリファレンス](https://platform.openai.com/docs/models)

---

## 英語READMEについて

国際的な利用を想定する場合は、英語版READMEもご用意ください。