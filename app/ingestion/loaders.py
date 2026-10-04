from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_core.documents import Document

from app.core.config import settings
from app.core.logging import get_logger, setup_logging

logger = get_logger(__name__)


def load_website(url: str | None = None) -> list[Document]:
    url = url or settings.portfolio_url
    loader = WebBaseLoader(url, bs_get_text_kwargs={"separator": "\n", "strip": True})
    docs = loader.load()
    chars = sum(len(d.page_content) for d in docs)
    logger.info("Website loaded: %d document(s), %d characters", len(docs), chars)
    return docs


def load_resume(path: Path | None = None) -> list[Document]:
    path = path or settings.resume_path
    docs = PyPDFLoader(str(path)).load()
    logger.info("Resume loaded: %d page(s)", len(docs))
    return docs


if __name__ == "__main__":
    setup_logging()

    web_docs = load_website()
    logger.info("Website preview:\n%s", web_docs[0].page_content[:1500])

    if settings.resume_path.exists():
        resume_docs = load_resume()
        logger.info("Resume preview:\n%s", resume_docs[0].page_content[:1000])
    else:
        logger.warning("Resume not found at %s", settings.resume_path)