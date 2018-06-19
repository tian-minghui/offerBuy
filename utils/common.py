# -*- coding:utf-8 -*-
import logging
import time
logger = logging.getLogger(__name__)


def retry(times=2):
    def _retry(func):
        def __retry(*args, **kwargs):
            ret = None
            for i in range(times):
                ret = func(*args, **kwargs)
                if ret:
                    return ret
            return ret

        return __retry

    return _retry


def get_time(add=0):
    return int(round(time.time() * 1000))+add