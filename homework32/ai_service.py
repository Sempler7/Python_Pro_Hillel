import os

from openai import AsyncOpenAI
from settings import OPENROUTER_API_KEY



client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)


styles = {
    "cyberpunk": (
        "Перепиши текст у стилі кіберпанк. "
        "Відповідь має бути короткою, атмосферною і трохи футуристичною."
    ),
    "viking": (
        "Перепиши текст у стилі вікінга. "
        "Відповідь має звучати сміливо, епічно і просто."
    ),
    "robot": (
        "Перепиши текст у стилі саркастичного робота з майбутнього. "
        "Використовуй технічні терміни, трохи іронії та звертайся до людини "
        "як до органічної істоти. Відповідь має бути короткою і дотепною."
    ),
    "business": (
        "Перепиши текст у діловому стилі. "
        "Відповідь має бути ввічливою, зрозумілою і професійною."
    ),
    "meme": (
        "Перепиши текст у мемному стилі. "
        "Відповідь має бути смішною, простою і сучасною."
    ),
}


async def generate_text(style: str, user_text: str) -> str:
    """
    Генерує текст у заданому стилі за допомогою OpenRouter API."""

    prompt = f"{styles[style]}\n\nТекст: {user_text}"

    response = await client.chat.completions.create(
        model="inclusionai/ring-2.6-1t:free",
        messages=[
            {
                "role": "system",
                "content": "Ти AI-асистент для стилізації тексту.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response.choices[0].message.content
