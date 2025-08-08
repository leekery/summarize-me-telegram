from typing import List, Dict
from openai import OpenAI
from config import settings
from bot.utils.text import normalize_for_telegram

DEEPSEEK_API_KEY = settings.deepseek_api_key
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

SYSTEM_PROMPT = (
    "Ты отвечаешь на вопросы по контексту переписки. Коротко, по делу, без канцелярита. "
    "Сначала ищи ответ в контексте; если его нет — используй общие знания, но явно пометь: "
    "«(дополнение не из чата)». Вывод — обычный ПЛЕЙН-ТЕКСТ без Markdown/HTML."
)

async def ask_with_context(msgs: List[Dict], question: str) -> str:
    if not DEEPSEEK_API_KEY:
        return "⚠️ API-ключ DeepSeek не настроен."

    # Контекст из переписки
    context = "\n".join(f"{m['user_name']}: {m['text']}" for m in msgs)

    user_prompt = (
        "Контекст чата (каждая строка «Имя: текст»):\n"
        f"{context}\n\n"
        f"Вопрос: {question}\n\n"
        "Требования к ответу:\n"
        "- обычный текст, без Markdown/HTML;\n"
        "- кратко, естественно;\n"
        "- если информации нет в контексте — дополни общими знаниями и пометь «(дополнение не из чата)»."
    )

    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            stream=False,
        )
        raw = resp.choices[0].message.content or ""
        return normalize_for_telegram(raw)
    except Exception as e:
        return normalize_for_telegram(f"Не удалось получить ответ: {e}")
