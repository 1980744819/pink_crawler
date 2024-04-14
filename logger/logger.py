from loguru import logger

logger.add("log/info.log", rotation="10 MB", level="INFO")
logger.add("log/warning.log", rotation="10 MB", level="WARNING")
logger.add("log/error.log", rotation="10 MB", level="ERROR")
