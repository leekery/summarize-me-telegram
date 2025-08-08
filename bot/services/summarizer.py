from typing import List, Dict
from openai import OpenAI
from config import settings

DEEPSEEK_API_KEY = settings.deepseek_api_key
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

SYSTEM_PROMPT = (
    "Ты — помощник, который составляет краткие и информативные сводки "
    "на основе переписки в чате. Не упоминай саму задачу создания сводки, "
    "просто выдай итог разговора."
)

# Инициализация клиента
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

async def summarize_messages(msgs: List[Dict]) -> str:
    """
    Получает список сообщений и возвращает краткую сводку с помощью DeepSeek API (OpenAI SDK).
    Если API недоступно или ключ пустой — возвращает заглушку.
    """
    if not DEEPSEEK_API_KEY:
        return _fallback_summary(msgs)

    # Формируем входные данные
    content = "\n".join(
        f"[{m['timestamp']}] {m['user_name']}: {m['text']}" for m in msgs
    )

    try:
        # Вызов DeepSeek
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": content},
            ],
            stream=False
        )
        content = response.choices[0].message.content
        return content.strip() if content is not None else ""

    except Exception as e:
        return f"(Ошибка подключения)\n{_fallback_summary(msgs)}\n\n{e}"

def _fallback_summary(msgs: List[Dict]) -> str:
    """Простейшая заглушка — последние 10 сообщений."""
    lines = [f"{m['user_name']}: {m['text']}" for m in msgs]
    summary = "\n".join(lines[-10:])
    return "📝 (заглушка):\n" + summary