from typing import List, Dict

# msgs: [{"user_name": "...", "text": "...", "timestamp": "..."}]
async def summarize_messages(msgs: List[Dict]) -> str:
    # TODO: заменить на реальный запрос к API DeepSeek
    lines = [f"{m['user_name']}: {m['text']}" for m in msgs[-10:]]
    return "📝 Краткая сводка (заглушка):\n" + "\n".join(lines)