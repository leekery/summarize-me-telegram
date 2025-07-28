import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    bot_token: str
    admin_id: int
    deepseek_api: str
    db_path: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            bot_token=os.environ["BOT_TOKEN"],
            admin_id=int(os.environ["ADMIN_ID"]),
            deepseek_api=os.environ["DEEPSEEK_API_KEY"],
            db_path=os.environ["DB_PATH"]
        )
    
settings = Settings.from_env()

# How to use | dataclass
# from config import settings
# token = settings.bot_token