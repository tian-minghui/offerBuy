import hashlib

from django.http import HttpResponse
from django.shortcuts import render
from offerBuy.config.config import ACCT_TOKEN

import logging

from offerBuyAcct.bo.Message import Message, MsgType
from offerBuyAcct.bo.replyText import replyText, WELCOME
# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# 处理微信服务器请求
def wei_xin(request):
    if request.method == 'GET':
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr')
        l = [ACCT_TOKEN, timestamp, nonce]
        l.sort()
        s = ''.join(l)
        sha1 = hashlib.sha1()
        sha1.update(s.encode('utf-8'))
        if sha1.hexdigest() == signature:
            logger.info('认证成功')
            return HttpResponse(echostr)
        else:
            logger.debug('认证失败 %s' % request.GET)
            return HttpResponse('error')
    if request.method == 'POST':
        data = request.body
        message = Message.parse_xml(data)
        if not message:
            return render(request, 'reply_text.xml', 'an unsupported command')
        if message.msg_type == MsgType.TEXT:
            pass

        if message.msg_type == MsgType.EVENT and message.event == 'subscribe':
            reply_text = replyText(message.user_id, message.self_user_id, WELCOME)
            return render(request, 'reply_text.xml', reply_text.get_dict())

        return render(request, 'reply_text.xml', 'an unsupported command')
