# -*- coding:utf-8 -*-
import time
from offerBuy.config.config import HEADERS, IP
from offerBuyAcct.taobao.session import login_session
from utils.httputils import check_resp
import logging

logger = logging.getLogger(__name__)


def get_item_list(item_url):
    url = 'http://pub.alimama.com/items/search.json'
    timestamp = int(round(time.time() * 1000))
    pvid = "10_123.122.140.198_2799_" + str(timestamp - 20000)
    params = {
        "q": item_url,
        "_t": timestamp - 1,
        "auctionTag": "",
        "perPageSize": "50",
        "shopTag": "",
        "t": timestamp,
        "_tb_token_": login_session.cookies.get("_tb_token_", domain=".alimama.com"),
        "pvid": pvid
    }
    req = login_session.Request('GET', url, params=params)
    r = req.prepare()
    head = {
        'X-Requested-With': 'XMLHttpRequest',
        'Host': 'pub.alimama.com',
        'Referer': r.url
    }
    resp = login_session.get(url, headers=head, params=params, allow_redirects=False)
    try:
        if check_resp(resp, url):
            item_list = resp.json()['data']['pageList']
            if item_list.length == 0:
                return
            return item_list, pvid
        else:
            return
    except KeyError as error:
        logging.error(url, error)
        return


def get_item_link(item, pvid):
    pass
