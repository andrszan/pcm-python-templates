import logging


def configure_logging(log_level: str) -> None:
    logger = logging.getLogger("app")
    logger.setLevel(log_level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s %(name)s %(message)s"))
        logger.addHandler(handler)
    logger.propagate = False
