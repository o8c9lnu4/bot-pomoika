import os
from dataclasses import dataclass


@dataclass
class BotConfig:
    bot_token: str
    base_url: str


def load_config() -> BotConfig:
    from dotenv import load_dotenv

    load_dotenv()
    token = os.getenv("BOT_TOKEN", "")
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set. Put it in .env or environment.")

    return BotConfig(bot_token=token, base_url=base_url)
