from app.core.config import settings
from app.core.logging import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)

logger.info("Qdrant URL: %s", settings.qdrant_url)
logger.info("Qdrant key loaded: %s", bool(settings.qdrant_api_key))
logger.info("Groq key loaded: %s", bool(settings.groq_api_key))


logger.info(
    "Langfuse keys loaded: %s",
    bool(settings.langfuse_public_key and settings.langfuse_secret_key),
)
logger.info("Langfuse base URL: %s", settings.langfuse_base_url)