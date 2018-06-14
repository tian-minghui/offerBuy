
import logging
logger = logging.getLogger(__name__)


def check(resp,url,status_code=200):
    if resp.status_code!=status_code:
        logger.error(url+"-----"+resp.status_code)
        return False
    return True


def retry(arg):
    def _retry(func):
        def __retry(*args,**kwargs):
            for i in range(arg):
                ret=func(*args,**kwargs)
                if ret:
                    return ret
            return ret
        return __retry
    return _retry