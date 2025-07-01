from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_base_url: str
    openai_api_key: SecretStr
    tg_token: SecretStr
    tg_owner_id: int
    tg_chat_id: int
    response_chance: float
    max_input_msgs: int = 30

    model_config = SettingsConfigDict(env_prefix='', env_file='.env')

settings = Settings()

sys_prompt: str
with open("prompt.txt") as f:
    sys_prompt = f.read()
