import requests

from offerBuy.config.config import HEADERS, IP
from utils.httputils import check_resp
from utils.common import retry
import logging
logger = logging.getLogger(__name__)


class LoginSession(requests.Session):
    def __init__(self):
        super().__init__()
        self.headers.update(HEADERS)
        LoginSession.alimama_init()
        LoginSession.login()

    @retry
    def alimama_init(self):
        url = 'http://pub.alimama.com/'
        head = dict()
        head["Host"] = "pub.alimama.com"
        head["Upgrade-Insecure-Requests"] = "1"
        resp = self.get(url, headers=head)
        return check_resp(resp, url)

    @retry
    def login(self):
        url = 'https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Flogin.taobao.com%2Fmember%2Ftaobaoke%2Flogin.htm%3Fis_login%3D1'
        print(self.cookies)
        data = {
            "TPL_username": "tb677116_88",
            "TPL_password": "",
            "ncoSig": "",
            "ncoSessionid": "",
            "ncoToken": "b9300c5bcacc946ad57fab4cf3bed61777ff3ec5",
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
            "TPL_password_2": "03aba1d2463114618d148133ef2b43a8b63a948acbcb83c27fefd10d3622d00cfe3f86755acf3a6f5a6af85d677760a29d8414266d286c640df4e53c3f5d848dc510951199dde27ec0627620d560cd42445b9d1a9abfcb3e151724ed4fa1922bd4d1d6d2996b0f120d1f7f2cf22ffa16b90b0799e05e1cd15a3eb94349927469",
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
        return check_resp(resp, url)

    def refresh(self):
        self.__init__()


login_session = LoginSession()

if __name__ == '__main__':
    pass
    # ali = Client()
    # ali.alimama_init()
    # ali.login()
    # ali.get_item_list(
    #     "https://item.taobao.com/item.htm?spm=a1z10.4-c-s.w11739546-18467978978.5.45fc7b8dyuxfoU&id=560234787224&scene=taobao_shop")
