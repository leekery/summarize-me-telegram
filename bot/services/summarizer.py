from typing import List, Dict

async def summarize_messages(msgs: List[Dict]) -> str:
    """
    Получает список сообщений и возвращает краткую сводку.
    Пока используется заглушка, которая просто склеивает последние строки.
    """
    lines = [f"{m['user_name']}: {m['text']}" for m in msgs]
    summary = "\n".join(lines[-10:])  # последние 10 сообщений
    return "📝 Краткая сводка:\n" + summary
