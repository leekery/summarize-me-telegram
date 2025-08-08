from typing import List, Dict
from openai import OpenAI
from config import settings

DEEPSEEK_API_KEY = settings.deepseek_api_key
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

SYSTEM_PROMPT = (
    "Ты — помощник, который отвечает на вопросы по переписке в чате, "
    "используя только достоверные сведения из контекста и общие знания. "
    "Если в переписке нет ответа — используй свой общий опыт, но укажи, "
    "что это не из чата."
)

async def ask_with_context(msgs: List[Dict], question: str) -> str:
    if not DEEPSEEK_API_KEY:
        return "⚠️ API-ключ DeepSeek не настроен."

    # Контекст из переписки
    context = "\n".join(f"{m['user_name']}: {m['text']}" for m in msgs)

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Контекст чата:\n{context}\n\nВопрос: {question}"},
            ],
            stream=False
        )
        content = response.choices[0].message.content
        return content.strip() if content is not None else ""

    except Exception as e:
        return f"Ошибка при обращении к DeepSeek: {e}"
