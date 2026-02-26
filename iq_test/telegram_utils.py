"""
Telegram bot orqali xabar yuborish.
Test natijasi chiqqanda guruhga ism, yosh, telefon va natija yuboriladi.
"""

import json
import logging
import urllib.request
import urllib.error
from django.conf import settings

logger = logging.getLogger(__name__)


def send_result_to_telegram(info, result):
    """
    Test natijasi chiqqanda guruhga ism, yosh, telefon va natijani yuboradi.
    info: dict with keys name, age, phone (session'dan)
    result: UserResult obyekti (score, correct_count, total_questions)
    Sozlamalar bo'lmasa yoki xatolik bo'lsa jim turadi (exception chiqarmaydi).
    """
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None) or ''
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', None) or ''
    token = token.strip() if isinstance(token, str) else ''
    chat_id = str(chat_id).strip() if chat_id is not None else ''

    if not token or not chat_id:
        logger.warning(
            "Telegram: xabar yuborilmadi. TELEGRAM_BOT_TOKEN=%s, TELEGRAM_CHAT_ID=%s. "
            ".env faylida o'zgaruvchilarni tekshiring.",
            'bor' if token else 'yo\'q',
            'bor' if chat_id else 'yo\'q',
        )
        return

    name = info.get('name', '-')
    age = info.get('age', '-')
    phone = info.get('phone', '-')

    text = (
        "🆕 IQ Test — yangi natija\n\n"
        f"👤 Ism: {name}\n"
        f"📅 Yosh: {age}\n"
        f"📱 Telefon: {phone}\n\n"
        f"📊 Ball: {result.score}\n"
        f"✅ To'g'ri javoblar: {result.correct_count} / {result.total_questions}"
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST', headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = resp.read().decode('utf-8', errors='replace')
            if resp.status != 200:
                logger.warning("Telegram API javob kodi %s: %s", resp.status, body[:200])
                return
            try:
                data = json.loads(body)
                if not data.get('ok'):
                    logger.warning("Telegram API ok=False: %s", body[:300])
            except json.JSONDecodeError:
                pass
    except (urllib.error.URLError, OSError, Exception) as e:
        logger.exception("Telegram xabar yuborishda xatolik: %s", e)
