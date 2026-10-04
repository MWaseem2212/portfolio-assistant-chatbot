from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    groq_api_key: str = ""
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_base_url: str = ""
    smtp_user: str = ""
    smtp_app_password: str = ""
    notify_to_email: str = ""
    allowed_origins: str = "http://localhost:3000"
    log_level: str = "INFO"

    portfolio_url: str = "https://waseem-portfolio-mocha.vercel.app/"
    resume_path: Path = BASE_DIR / "data" / "raw" / "resume.pdf"

settings = Settings()