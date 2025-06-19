import pandas as pd
import io
from typing import List, Dict, Any

def export_paired_messages_to_csv(paired_messages: List[Dict[str, Any]]) -> str:
    """
    チャット履歴（ペアメッセージ）をCSV形式の文字列に変換する。

    Args:
        paired_messages (List[Dict]): チャット履歴のリスト

    Returns:
        str: CSV形式の文字列（utf-8-sig, カラム順固定）
    """
    if not paired_messages or not isinstance(paired_messages, list):
        return ""

    # ネストした'dict'があればフラット化
    flat_messages = []
    for msg in paired_messages:
        if isinstance(msg, dict):
            # 'message'キーがあればその値を使う
            if "message" in msg and isinstance(msg["message"], dict):
                flat_messages.append(msg["message"])
            else:
                flat_messages.append(msg)
    if not flat_messages:
        return ""

    df = pd.DataFrame(flat_messages)
    columns = [
        "assistant_id",
        "thread_id",
        "created_at",
        "user_input",
        "output",
        "Total_Tokens",
        "Completion_Tokens",
        "Prompt_Tokens"
    ]
    # 必要なカラムがなければ空文字で補完
    for col in columns:
        if col not in df.columns:
            df[col] = ""
    df = df[columns]
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
    return csv_buffer.getvalue()