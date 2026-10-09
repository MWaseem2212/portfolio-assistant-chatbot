from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import settings
from app.core.logging import get_logger , setup_logging

logger = get_logger(__name__)

def chunk_documents(docs: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        add_start_index=True
    )
    chunks = splitter.split_documents(docs)
    logger.info("Split %d documents(s) into %d chunk(s)", len(docs), len(chunks))
    return chunks


if __name__ == "__main__":
    from app.ingestion.cleaning import clean_documents
    from app.ingestion.loaders import load_resume, load_website

    setup_logging()
    docs = clean_documents(load_website() + load_resume())
    chunks = chunk_documents(docs)

    sizes = [len(c.page_content) for c in chunks]
    logger.info(
        "Chunk sizes: min=%d, max=%d, avg=%d",
        min(sizes),
        max(sizes),
        sum(sizes) // len(sizes),
    )
    for i, chunk in enumerate(chunks[:3]):
        logger.info(
            "Chunk %d (start=%s):\n%s", i, chunk.metadata.get("start_index"), chunk.page_content
        )