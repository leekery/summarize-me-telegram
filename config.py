import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()
# Comment this block to use pydantic
@dataclass(frozen=True)
class Settings:
    bot_token: str
    admin_id: int
    deepseek_api: str
    db_path: str
    default_limit: int

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            bot_token=os.environ["BOT_TOKEN"],
            admin_id=int(os.environ["ADMIN_ID"]),
            deepseek_api=os.environ["DEEPSEEK_API_KEY"],
            db_path=os.environ["DB_PATH"],
            default_limit=int(os.environ["DEFAULT_LIMIT"])
        )
settings = Settings.from_env()

# How to use | dataclass
# from config import settings
# token = settings.bot_token
# print(token)

# Commnet this block to use dataclass
# from pydantic_settings import BaseSettings
# class Settings(BaseSettings):
#     bot_token: str
#     admin_id: int
#     deepseek_api_key: str
#     db_path: str
#     default_limit: int

#     model_config = {
#         "env_file": ".env",
#         "extra": "ignore",
#     }

# settings = Settings() # type: ignore

# How to use | pydantic
# from config import settings
# token = settings.bot_token
