"""
item
"tkSpecialCampaignIdRateMap": {
                    "8013864": "7.00",
                    "12528500": "7.00",
                    "13021516": "7.00",
                    "13804894": "5.50"
                },
                "leafCatId": 50000557,
                "rootCatScore": 0,
                "debugInfo": null,
                "eventCreatorId": 0,
                "rootCatId": 30,
                "title": "太平鸟男装 冬季新款 时尚刺绣圆领长袖毛衫针织衫毛衣BWEB74514",
                "userType": 0,
                "nick": "太平鸟男装风尚馆",
                "couponInfo": "无",
                "hasUmpBonus": null,
                "umpBonus": null,
                "isBizActivity": null,
                "shopTitle": "太平鸟男装官方店",
                "pictUrl": "//img.alicdn.com/bao/uploaded/i3/2166356588/TB2ussso5CYBuNkHFCcXXcHtVXa_!!2166356588.jpg",
                "sellerId": 2166356588,
                "couponLink": "",
                "couponLinkTaoToken": "",
                "couponAmount": 0,
                "couponStartFee": 0,
                "couponTotalCount": 0,
                "couponLeftCount": 0,
                "tkCommonRate": 5.5,
                "tkCommonFee": 16.45,
                "rlRate": 54.55,
                "hasRecommended": null,
                "hasSame": null,
                "sameItemPid": "-1506389454",
                "tkFinalRate": null,
                "eventRate": null,
                "rootCategoryName": null,
                "couponOriLink": null,
                "auctionId": 560234787224,
                "couponActivityId": null,
                "tkRate": 5.5,
                "reservePrice": 658,
                "couponShortLink": null,
                "userTypeName": null,
                "tkFinalFee": null,
                "couponEffectiveStartTime": "",
                "couponEffectiveEndTime": "",
                "biz30day": 1,
                "includeDxjh": 1,
                "tkCommFee": 16.45,
                "totalFee": 0,
                "totalNum": 0,
                "zkPrice": 299,
                "auctionTag": "385 587 907 1163 1483 2059 2123 3851 4491 4550 4555 6603 11083 11339 11531 12491 13707 13771 15563 17739 17803 25282 25729 27137 28353 30977 34305 35521 36161 40897 41153 50370 52290 61890 63297 66241 67521 70465 79041 85249 85313 92481 95233 96321 104514 215810 217346 235202 249858",
                "auctionUrl": "http://item.taobao.com/item.htm?id=560234787224",
                "dayLeft": -17696,
                "tk3rdRate": null,
                "tkMktStatus": null
"""
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
