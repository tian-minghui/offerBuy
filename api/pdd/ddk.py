from api.pdd.pdd_utils import send_request
import logging
from api.pdd.ddkVo import GoodsVo, Pid, PromotionInfo

logger = logging.getLogger('django')

goods_search_type = "pdd.ddk.goods.search"
pid_query_type = "pdd.ddk.goods.pid.query"
pid_generate_type = "pdd.ddk.goods.pid.generate"
promotion_url_generate_type = "pdd.ddk.goods.promotion.url.generate"


def response_check(response):
    if response.status_code != 200:
        logger.error("error when item search status_code:" + response.status_code)
        return False
    else:
        if "error_response" in response.json().keys():
            logger.error("error when item search error_response")
            logger.error(response.json())
            return False
        else:
            return True


def item_search(goods_word):
    """
    根据商品关键词查 商品
    :param goods_word:
    :return: list<GoodsVo>
    """
    params = {
        "type": goods_search_type,
        "sort_type": 0,
        "with_coupon:": "false",
        "keyword": goods_word
    }
    response = send_request(params)
    if response_check(response):
        goods_list = []
        for goods_json in response.json()["goods_search_response"]["goods_list"]:
            goods_list.append(GoodsVo(goods_json))
        return goods_list
    return None


def pid_search():
    """
    查询已经生成的推广位信息
    :return: list  [
      {
        "p_id": "81_1812886",
        "create_time": 1517724155
      },
      {
        "p_id": "81_1812888",
        "create_time": 1517916590
      }]
    """
    params = {
        "type": goods_search_type,
    }
    response = send_request(params)
    if response_check(response):
        return response.json()["p_id_query_response"]["p_id_list"]
    return None


def pid_generate(p_id_name):
    """

    :param p_id_name:
    :return: Pid
    """
    params = {
        "type": pid_generate_type,
        "number": 1,
        "p_id_name_list": [p_id_name]
    }
    response = send_request(params)
    if response_check(response):
        d = response.json()["p_id_generate_response"]["p_id_list"][0]
        return Pid(d["p_id_name"], d["p_id"])


def promotion_url_generate(p_id, goods_id,
                           is_multi_group=True,
                           is_generate_short_url=True,
                           is_generate_weapp_webview=True,
                           is_generate_we_app=True,
                           custom_parameters=None):
    """

    :param p_id: 推广位ID
    :param goods_id: 商品ID
    :param is_multi_group: true--生成多人团推广链接 false--生成单人团推广链接（默认false）
    :param is_generate_short_url: 是否生成短链接，true-是，false-否
    :param is_generate_weapp_webview: 是否生成唤起微信客户端链接，true-是，false-否，默认false
    :param is_generate_we_app: 是否生成小程序推广
    :return: PromotionInfo
    """
    params = {
        "type": promotion_url_generate_type,
        "p_id": p_id,
        "multi_group" : is_multi_group,
        "goods_id_list": [goods_id],
        "generate_short_url": is_generate_short_url,
        "generate_weapp_webview": is_generate_weapp_webview,
        "generate_we_app": is_generate_we_app
    }
    if custom_parameters:
        params["custom_parameters"] = custom_parameters
    response = send_request(params)
    if response_check(response):
        d = response.json()["goods_promotion_url_generate_response"]["goods_promotion_url_list"][0]
        return PromotionInfo(d)


if __name__ == '__main__':
    word = "珊瑚绒浴帽女加厚干发帽超强吸水圆形浴帽干发巾速干舒适"
    goods = item_search(word)
    print(goods[0].category_name)
