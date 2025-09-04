import os
from dataclasses import dataclass


@dataclass
class BotConfig:
    bot_token: str
    admin_ids: tuple[int, ...]
    webapp_url: str | None = None


def load_config() -> BotConfig:
    from dotenv import load_dotenv

    load_dotenv()
    token = os.getenv("BOT_TOKEN", "")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set. Put it in .env or environment.")

    admin_ids_str = os.getenv("ADMIN_IDS", "")
    admin_ids: tuple[int, ...] = tuple(
        int(x) for x in admin_ids_str.split(",") if x.strip().isdigit()
    )

    webapp_url = os.getenv("WEBAPP_URL") or None
    return BotConfig(bot_token=token, admin_ids=admin_ids, webapp_url=webapp_url)
