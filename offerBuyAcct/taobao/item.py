import time
from offerBuy.config.config import HEADERS, IP
from offerBuyAcct.taobao.session import login_session
from utils.httputils import check_resp
from utils.common import get_time
import logging
import requests

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
            if len(item_list) == 0:
                return
            return item_list, pvid
        else:
            return
    except KeyError as error:
        logging.error(url, error)
        return


def get_item_link(auctionId, adzoneid, siteid, pvid):
    logger.info('the auctionId is %s' % auctionId)
    url = 'http://pub.alimama.com/common/code/getAuctionCode.json'
    params = {
        'auctionid': auctionId,
        'adzoneid': adzoneid,
        'siteid': siteid,
        'scenes': '1',
        't': get_time(),
        '_tb_token_': login_session.cookies.get("_tb_token_", domain=".alimama.com"),
        'pvid': pvid
    }
    resp = login_session.get(url, params=params, allow_redirects=False)
    if not check_resp(resp, url):
        logger.error(resp.content)
        logger.error(resp.json())
    return resp.json()


def get_first_item(item_url):
    from offerBuy.config.config import ADZONE_ID, SITE_ID
    from offerBuyAcct.bo.item import Item
    first_dict, pvid = get_item_list(item_url)[0]
    auctionid = first_dict['auctionid']
    item = Item(auctionid, first_dict['title'], first_dict['pictUrl'], first_dict['tkCommonRate'],
                first_dict['zkPrice'], first_dict['tkCommFee'])
    link_dict = get_item_link(auctionid, ADZONE_ID, SITE_ID, pvid)['data']
    item.set_link(link_dict['clickUrl'], link_dict['taoToken'], link_dict['shortLinkUrl'])
    return item


if __name__ == '__main__':
    from offerBuy.config.config import ADZONE_ID, SITE_ID

    item_list, pvid = get_item_list(
        'https://item.taobao.com/item.htm?spm=a1z10.4-c-s.w11739546-18467978978.5.45fc7b8dyuxfoU&id=560234787224&scene=taobao_shop')
    print(item_list)
    auctionid = item_list[0]['auctionId']
    get_item_link(auctionid, ADZONE_ID, SITE_ID, pvid)
