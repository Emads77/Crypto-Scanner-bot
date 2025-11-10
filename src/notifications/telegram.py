import httpx
import logging

class TelegramNotifier:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base = f"https://api.telegram.org/bot{bot_token}"

    def send(self, text: str) -> None:
        try:
            r = httpx.post(
                f"{self.base}/sendMessage",
                json={"chat_id": self.chat_id, "text": text, "parse_mode": "HTML"},
                timeout=10.0,
            )
            r.raise_for_status()
        except Exception as e:
            logging.exception("Telegram send failed: %s", e)