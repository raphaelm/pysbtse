import logging
import time
from functools import wraps


def log_execution(f):
    logger = logging.getLogger(f.__module__)

    @wraps(f)
    def wrapper(*args, **kwargs):
        logger.debug(f"{f.__name__} called")
        t = time.time()
        try:
            r = f(*args, **kwargs)
        except:
            logger.debug(f"{f.__name__} failed in {time.time() - t}s")
            raise
        else:
            logger.debug(f"{f.__name__} returned in {time.time() - t}s")
        return r
    return wrapper