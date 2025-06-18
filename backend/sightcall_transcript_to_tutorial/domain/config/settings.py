from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field(validation_alias="DATABASE_URL")
    github_client_id: str = Field(validation_alias="GITHUB_CLIENT_ID")
    github_client_secret: str = Field(validation_alias="GITHUB_CLIENT_SECRET")
    github_callback_url: str = Field(validation_alias="GITHUB_CALLBACK_URL")
    frontend_url: str = Field(validation_alias="FRONTEND_URL")
    jwt_secret: str = Field(validation_alias="JWT_SECRET")
    jwt_algorithm: str = Field(validation_alias="JWT_ALGORITHM")
    openai_api_key: str = Field(validation_alias="OPENAI_API_KEY")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow",
    }


settings = Settings()  # type: ignore[call-arg]
