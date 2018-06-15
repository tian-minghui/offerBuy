# -*- coding:utf-8 -*-
import logging

logger = logging.getLogger(__name__)


def retry(times=3):
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
