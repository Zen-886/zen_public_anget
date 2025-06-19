# Zen_public_agent

## Overview
Zen_public_agent is a chatbot web application powered by the OpenAI API and Streamlit.  
Users can input their OpenAI API key, select from multiple models, and interact with the assistant in a simple web UI.

## Features
- Simple web chat UI built with Streamlit
- Supports various OpenAI models (gpt-4.5-preview, gpt-4o, etc.)
- API key management via `.env` file (**Never share your API key publicly**)
- Docker/DevContainer support
- Chat history export to CSV (via extension pages)

## Setup

### 1. Requirements
- Python 3.11 or higher
- pip
- OpenAI API key ([Get yours here](https://platform.openai.com/account/api-keys))

### 2. Clone & Install

```bash
git clone https://github.com/your-username/Zen_public_agent.git
cd Zen_public_agent
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Create `.env` File

Create a `.env` file in the project root and add your API key as follows:  
**No spaces or quotes are needed.**

```
OPENAI_API_KEY=your_openai_api_key_here
```

**Do not commit your `.env` file to any public repository. Add it to `.gitignore`.**

### 4. Launch the App

```bash
streamlit run chatbot.py
```

To use extension features, specify the files in the `pages/` directory.

---

## Main Files

- `chatbot.py` … Main chatbot application
- `requirements.txt` … Python dependencies
- `pages/` … Extension features (see below)
- `.devcontainer/Dockerfile` … DevContainer Dockerfile
- `common_utils.py` … Utilities for chat history export

### Main files in `pages/` directory
- `A_set_assistant_id.py` … Chat with a specified assistant ID
- `A_set_api_key_assistant_id.py` … Chat with both API key and assistant ID specified
- `B_export_history.py` … Export chat history as CSV

---

## Chat History Export

On the `B_export_history.py` page, you can download your chat history as a CSV file.  
The export includes user/assistant messages and timestamps.

---

## Security & Notes

- **Never share your API key or assistant ID publicly.**  
  Always add `.env` and any sensitive files to `.gitignore` to prevent accidental leaks.
- Using the OpenAI API may incur usage fees. Manage your API key and usage responsibly.
- While prompt injection and malicious input are difficult to fully prevent, consider filtering or limiting input length as needed.

---

## License

This project is licensed under the MIT License.  
See the `LICENSE` file for details.

---

## References

- [Streamlit Documentation](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps)
- [OpenAI APIリファレンス](https://platform.openai.com/docs/models)
