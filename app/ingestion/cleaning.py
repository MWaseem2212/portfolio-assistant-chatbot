import re
from langchain_core.documents import Document
from app.core.logging import get_logger, setup_logging

logger = get_logger(__name__)

DECORATIVE_SYMBOLS = re.compile(r"[◆▹]")
MIN_REPEAT_BLOCK = 4

def drop_repeated_blocks(lines: list[str], min_len: int = MIN_REPEAT_BLOCK) -> list[str]:
    result: list[str] = []
    i=0
    while i < len(lines):
        max_len = (len(lines) - i) // 2
        for size in range(max_len, min_len - 1, -1):
            block = lines[i: i + size]
            if block == lines[i + size: i + 2 * size]:
                result.extend(block)
                i += size
                while lines[i : i + size] == block:
                    i += size
                break

        else:
            result.append(lines[i])
            i += 1
    return result

def clean_text(text: str) -> str:
    text = DECORATIVE_SYMBOLS.sub("", text)
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    lines = drop_repeated_blocks(lines)
    return "\n".join(lines)

def clean_documents(docs: list[Document]) -> list[Document]:
    return [
        Document(page_content=clean_text(d.page_content), metadata=d.metadata)
        for d in docs
    ]

if __name__ == "__main__":
    from app.ingestion.loaders import load_website
    setup_logging()
    raw = load_website()
    cleaned = clean_documents(raw)
    before = sum(len(d.page_content) for d in raw)
    after = sum(len(d.page_content) for d in cleaned)
    logger.info("Characters: %d -> %d", before, after)
    logger.info("Cleaned preview:\n%s", cleaned[0].page_content[:1500])
    text = cleaned[0].page_content
    logger.info("Cleaned tail:\n%s", text[-1200:])
    for keyword in ["Axix", "Education", "DocuMind", "NexaAgent", "OpsPilot", "Contact"]:
        logger.info("%s found: %s", keyword, keyword in text)