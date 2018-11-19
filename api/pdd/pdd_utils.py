from api.pdd.settings import client_id, client_secret, http_url
from utils.common import get_time
import requests
import hashlib


def send_request(params):
    """
    根据传入的参数 生成请求
    :param params: dict
    :return: response
    """
    if isinstance(params, dict):
        params["client_id"] = client_id
        params["timestamp"] = get_time()
        sorted_params = sorted(params.items(), key=lambda item: item[0])
        tmp = client_secret
        for key, value in sorted_params:
            tmp += str(key) + str(value)
        tmp += client_secret
        md5 = hashlib.md5()
        md5.update(tmp.encode('utf-8'))
        sign = md5.hexdigest()
        params["sign"] = sign.upper()
        return requests.post(http_url, params)
    else:
        raise RuntimeError("error type")


if __name__ == '__main__':
    data = {
        'access_token': 'asd78172s8ds9a921j9qqwda12312w1w21211',
        'client_id': 1,
        'data_type': 'XML',
        'type': 'pdd.order.number.list.get',
        'timestamp': '1480411125',
        'order_status': '1',
        'page': '1',
        'page_size': '10'
    }
