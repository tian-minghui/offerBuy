import time
from api.taobao.session import login_session
from utils.httputils import check_resp
from utils.common import get_time
import logging
import requests
import random
from offerBuyAcct.bo.item import Item

logger = logging.getLogger('django')


def get_pvid():
    from offerBuy.config.config import IP
    timestamp = int(round(time.time() * 1000))
    return '10_' + IP + '_2799_' + str(timestamp - random.randint(2000, 20000))


# all =True  不勾选营销的定向计划
def search_items(search_condition, all=True):
    items = []
    url = 'http://pub.alimama.com/items/search.json'
    params = {
        "q": search_condition,
        "_t": get_time(-1),
        "auctionTag": "",
        "perPageSize": "50",
        "shopTag": "yxjh",
        "t": get_time(),
        "_tb_token_": login_session.cookies.get("_tb_token_", domain=".alimama.com"),
        "pvid": get_pvid()
    }
    if all:
        params['toPage'] = '1'
        params['shopTag'] = ''
    req = requests.Request('GET', url, params=params)
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
            if not item_list or len(item_list) == 0:
                logger.warn('返回结果为None')
                logger.warn(resp.json())
                return items
            for item in item_list:
                items.append(Item(item['auctionId'], item['title'], item['pictUrl'], item['tkCommonRate'],
                                  item['zkPrice'], item['tkCommFee']))
        return items
    except KeyError as error:
        logging.error(url, error)
        return items


def get_item_link(item, adzoneid, siteid):
    auctionId = item.auctionId
    logger.info('the auctionId is %s' % auctionId)
    url = 'http://pub.alimama.com/common/code/getAuctionCode.json'
    params = {
        'auctionid': auctionId,
        'adzoneid': adzoneid,
        'siteid': siteid,
        'scenes': '1',
        't': get_time(),
        '_tb_token_': login_session.cookies.get("_tb_token_", domain=".alimama.com"),
        'pvid': get_pvid()
    }
    resp = login_session.get(url, params=params, allow_redirects=False)
    if not check_resp(resp, url):
        logger.error(resp.content)
        logger.error(resp.json())
    js = resp.json()['data']
    item.set_link(js['clickUrl'], js['taoToken'], js['shortLinkUrl'])
    return item


def get_item_object(search_condition):
    pass


def get_first_item(item_url):
    from offerBuy.config.config import ADZONE_ID, SITE_ID
    item = None
    items = search_items(item_url)
    if items and len(items) != 0:
        item = get_item_link(items[0], ADZONE_ID, SITE_ID)
    return item


if __name__ == '__main__':
    from offerBuy.config.config import ADZONE_ID, SITE_ID

    pass
