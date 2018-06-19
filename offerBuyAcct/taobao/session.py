import requests

from offerBuy.config.config import HEADERS, IP
from utils.httputils import check_resp
from utils.common import retry, get_time
import logging
import re

logger = logging.getLogger(__name__)


def get_st_url(text):
    alibaba_pattern = 'https://passport\.alibaba\.com/mini_apply_st\.js.+callback=callback'
    alipay_pattern='https://passport\.alipay\.com/mini_apply_st\.js.+callback=callback'
    l1=re.findall(alibaba_pattern,text)
    l2=re.findall(alipay_pattern,text)
    if len(l1)==1 and len(l2)==1:
        return l1[0],l2[0]
    return None,None

class LoginSession(requests.Session):
    def __init__(self):
        super().__init__()
        self.headers.update(HEADERS)
        # self.alimama_init()
        # self.login()
        self.get_pub_context()

    def alimama_init(self):
        url = 'http://pub.alimama.com/'
        head = dict()
        head["Host"] = "pub.alimama.com"
        head["Upgrade-Insecure-Requests"] = "1"
        resp = self.get(url, headers=head)
        return check_resp(resp, url)

    def login(self):
        url = 'https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Flogin.taobao.com%2Fmember%2Ftaobaoke%2Flogin.htm%3Fis_login%3D1'
        data = {
            "TPL_username": "tb677116_88",
            "TPL_password": "",
            "ncoSig": "",
            "ncoSessionid": "",
            "ncoToken": "6e4c94851e2c7d3a63db7d6c0a40c9e34203b18f",
            "slideCodeShow": "false",
            "useMobile": "false",
            "lang": "zh_CN",
            "loginsite": "0",
            "newlogin": "0",
            "TPL_redirect_url": "http://login.taobao.com/member/taobaoke/login.htm?is_login=1",
            "from": "alimama",
            "fc": "default",
            "style": "mini",
            "css_style": "",
            "keyLogin": "false",
            "qrLogin": "true",
            "newMini": "false",
            "newMini2": "true",
            "tid": "",
            "loginType": "3",
            "minititle": "",
            "minipara": "",
            "pstrong": "",
            "sign": "",
            "need_sign": "",
            "isIgnore": "",
            "full_redirect": "true",
            "sub_jump": "",
            "popid": "",
            "callback": "",
            "guf": "",
            "not_duplite_str": "",
            "need_user_id": "",
            "poy": "",
            "gvfdcname": "10",
            "gvfdcre": "68747470733A2F2F7075622E616C696D616D612E636F6D2F696E6465782E68746D",
            "from_encoding": "",
            "sub": "",
            "TPL_password_2": "4a7a3f3ee76b09db768b9ad3820fde4ce00e1cdb9d5c889272271ab3cc5703cce5ede8ab21cefb43d9e4c3492f389ca2677cfda76949ec5cb069212f23d41f9aac481fd75468432db30a11fdf28a20e2d0748dd9df19ae3f0e88797088fe3bf58926d15f9712c2385acccb1f02f5a8dd90eb317cd9aa8071354b2425cde75d8d",
            "loginASR": "1",
            "loginASRSuc": "1",
            "allp": "",
            "oslanguage": "zh-CN",
            "sr": "2560*1440",
            "osVer": "",
            "naviVer": "chrome|66.0335917",
            "osACN": "Mozilla",
            "osAV": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36",
            "osPF": "Win32",
            "miserHardInfo": "",
            "appkey": "00000000",
            "nickLoginLink": "",
            "mobileLoginLink": "https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&from=alimama&redirectURL=http://login.taobao.com/member/taobaoke/login.htm?is_login=1&full_redirect=true&disableQuickLogin=true&useMobile=true",
            "showAssistantLink": "",
            "um_token": "HV01PAAZ0b828fbfdddf519c5b211a8300b44d6c",
            "ua": "109#k8/a7BOIapq3gjNhSBzpCzS6T4vERMZcCqXhh/WkNXkn/vJupc25hiD6pC51wtbcTvTDrghdwjWc2vLCrBGaajH4/1cC1ad+qU5RI5/gHwQp1vQ7yApEY0sxy7LnbEGaNR/wccYSacyeAngHuU2DJgrvENo96lza/No8PWimNLzcNuioaQkgedExkphWgvN1zUpR9WCuwbWNzt7eTakW1MYB0CQE27NEmg2IX6NDysbZCzs6iKO+uW4Fc5UsUdbyo14VDjEw9niSQ1+DLUYhh2dB25DtU9GKwyRVdj3UVMqMGkAcrLaxo5bzkW/ehkpRFdLzENU0cPoun1ZNLwkP1brReqUTRMyNfeDWzNS/1Qy3kpAKo7xKIA8A0X39fBwG75QTzth98Zzbh0bETBTapl9Ur6A1D7M4fsSQeTumTcWnDSGYgUMIGWnCli9SgUchn1E+5U8KRamofsCmz2aIGWYElszVt9UxrObLAUQpGuMMDVh77EgUz2QiMDrimu9/tZzLKa1H5erxi2cEtclor3hxld+qe6VI7D+tx1Rd/JoBAwT5LEpsq9YrnkUDY1ddGUNlCl8i67XsUrgydVpQ59jQgKMdKi3+gOVDpF5a+CEFz999227fKG5hR25v9iPCtCxfCJU/htyv5L3CdTvYD2CCa1CqYIEPQsRZj7jpVKiGGwdKd29wgsWoCuEdzk/1So/DCAuf6KYbysj6RSiP4fA9WxElmXQJOpRcTHV8+xjKC/QufgTFeU/6EIx/xW3YsrxThK3BE48Ptkmo/ENtcWf0DYsQ65pDBkoUDDp9p1EpbKjWf0242AvcR4O76FcQb8eVFQ/VEJcsxafsUS3xnO2u9ikAwkITW9+4sbX/YibQlIiwDGJrpRLZE7R853V/IYZ1zx9DRqBmNP3cuQjVVhXdq+SmhPLTwn4q8qGMgDZWhqEHZLwceL51tTi6N0b9AGHa5ISVvMFYgLOjw43tOQXeeCAala44/2h+lx+omV/h+uqovpjLzmHImlbHy9pwBoJe6oJn32ZhY/Eat72FJTnEhf5EgP4zuEoo9baD2erOmvl2uef8bK5Hmwo43X8xEnotJmmjgc6RuH7GNtUGAp35RsWVKH7UdxB5ikO6nnmZL6FlSSRFl2JyhR3dQuTBd0ERtCnRzzSDJXtYnRERY3LUcnIYSa=="
        }
        resp = self.post(url, data=data)
        if not check_resp(resp,url):
            return
        alibaba_url,alipay_url=get_st_url(resp.text)
        if alibaba_url and alipay_url:
            self.get(alibaba_url)
            self.get(alipay_url)
        else:
            logger.error(alibaba_url,alipay_url)
            return
        print(self.cookies)

        url1='https://www.alimama.com/membersvc/my.htm'
        params={
            'domain': 'taobao',
            'service': 'user_on_taobao',
            'sign_account': 'e86d40ed77c8d07efd4a02fbf5362b48'
        }
        resp=self.get(url1,params=params,allow_redirects=False)
        if not check_resp(resp,url1,status_code=302):
            print(resp.url)


        #
        # url2='https://login.taobao.com/aso/tgs'
        # params={
        #     'domain': 'alimama',
        #     'sign_account': 'e86d40ed77c8d07efd4a02fbf5362b48',
        #     'service': 'user_on_taobao',
        #     'target': '68747470733A2F2F7075622E616C696D616D612E636F6D2F696E6465782E68746D'
        # }
        # resp = self.get(url2, params=params, allow_redirects=False)
        # if not check_resp(resp, url2, status_code=302):
        #     print(resp.url)
        # url3='https://www.alimama.com/aso/tvs'
        # params={
        #     'domain': 'taobao',
        #     'sign_account': 'e86d40ed77c8d07efd4a02fbf5362b48',
        #     'target': '68747470733A2F2F7075622E616C696D616D612E636F6D2F696E6465782E68746D',
        #     'token': '3531666662353435376563613438663632396366346466343562396532356531',
        #     'sign_time': int(get_time()/1000),
        #     'defaultLoginURL': 'https://login.taobao.com/member/login.jhtml'
        # }
        # resp = self.get(url3, params=params, allow_redirects=False)
        # if not check_resp(resp, url3, status_code=302):
        #     print(resp.url)
        return check_resp(resp, url)

    def login_cookie(self):
        pass

    def refresh(self):
        self.__init__()

    def get_pub_context(self):
        self.cookies.update({
            'alimamapwag': 'TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzY2LjAuMzM1OS4xNzAgU2FmYXJpLzUzNy4zNg%3D%3D',
            'alimamapw': 'RVFXAQ5VVFA5Wl5qVFZRVwRVBgRRVAxTXFQFBFYAV1QGUFAFBgIHAggAAAQ%3D',
            'cna':'opiuEzNcEBICAd3fUfFnXB1L',
            't':'e0df263316062eb544a929f2ac394a07',
            'cookie2':'1cc7cd7aa3ea8d2b4c101c78e90c496f',
            'v':'0',
            'cookie32':'2c3be12e34a4db45d57a2d522915cff0',
            'cookie31':'MTMyMzAyMDU1LHRiNjc3MTE2Xzg4LHRpYW5taDIwMTNAMTYzLmNvbSxUQg%3D%3D',
            'login':'UtASsssmOIJ0bQ%3D%3D',
            'isg':'BBUVSj_T4nOoacaPrYBUDgv9JBEPushIkBaRY5e7vAzb7jbgXmah9J9nvPLYbuHc',
            '_tb_token_':'5663b4137373a'

        })
        url = 'https://pub.alimama.com/common/getUnionPubContextInfo.json'
        resp = self.get(url)
        data = resp.json()['data']
        if 'memberid' not in data.keys():
            logger.error('当前未登录')
            logger.error(resp.json())
            return False
        print(data)
        return True


login_session = LoginSession()

if __name__ == '__main__':
    login_session.get_pub_context()
