from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_base_url: str
    openai_api_key: str
    tg_token: str

    model_config = SettingsConfigDict(env_prefix='', env_file='.env')

settings = Settings()
