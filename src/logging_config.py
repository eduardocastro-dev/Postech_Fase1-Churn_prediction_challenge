import logging
import os


def configurar_logging() -> None:
    """Configura o logging da aplicação a partir de LOG_LEVEL."""
    nivel = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, nivel, logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
