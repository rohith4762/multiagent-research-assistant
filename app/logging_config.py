import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("research_assistant.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
