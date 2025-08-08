from typing import List, Dict
from openai import OpenAI
from config import settings
from bot.utils.text import normalize_for_telegram

DEEPSEEK_API_KEY = settings.deepseek_api_key
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# Инициализация клиента
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

SYSTEM_PROMPT = (
    "Ты делаешь краткие, естественные сводки переписки. Стиль — как сообщение в чате: "
    "коротко, по делу, нейтрально. Учитывай подписи к медиа (например: «Фото: …», «Стикер 😊»). "
    "Не добавляй преамбулу и выводы, не обращайся к собеседникам, не описывай, что ты ИИ. "
    "Формат вывода: обычный ПЛЕЙН-ТЕКСТ без Markdown и HTML, нумерованный список 3–6 пунктов."
)

async def summarize_messages(msgs: List[Dict]) -> str:
    if not DEEPSEEK_API_KEY:
        return _fallback_summary(msgs)

    context = "\n".join(f"{m['user_name']}: {m['text']}" for m in msgs)
    user_prompt = (
        "Вот фрагменты переписки (каждая строка — «Имя: текст»). "
        "Составь краткую естественную сводку:\n\n"
        f"{context}\n\n"
        "Требования к формату:\n"
        "1) Только обычный текст, без звёздочек, подчёркиваний и тегов.\n"
        "2) Нумерованный список (1., 2., 3., …) без лишних пустых строк.\n"
        "3) Если упоминаются медиа, используй вид «Фото: …», «Стикер 😊», «Видео: …».\n"
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
        return f"(Ошибка подключения)\n{_fallback_summary(msgs)}\n\n{e}"

def _fallback_summary(msgs: List[Dict]) -> str:
    lines = [f"{m['user_name']}: {m['text']}" for m in msgs[-6:]]
    numbered = "\n".join(f"{i+1}. {line}" for i, line in enumerate(lines))
    return f"Краткая сводка:\n{numbered}"