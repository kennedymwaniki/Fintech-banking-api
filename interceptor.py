from loguru import logger
import logging


class IntercerptorHandler(logging.Handler):
    def emit(self, record):
        try:
            # get level name
            level = logger.level(record.levelname).name

        except ValueError:
            level = record.levelno

        # here we get current stack frame to report logs origin
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
            # pass log messages to loguru
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )
