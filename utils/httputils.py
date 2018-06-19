# -*- coding:utf-8 -*-
import logging

logger = logging.getLogger(__name__)


def check_resp(resp, url, status_code=200):
    if resp.status_code != status_code:
        logger.error(url + "-----" + str(resp.status_code))
        return False
    return True
