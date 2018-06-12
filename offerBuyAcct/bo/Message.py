# -*- coding:utf-8 -*-
from xml.etree import ElementTree
from enum import Enum


class MsgType(Enum):
    TEXT = 'text'
    EVENT = 'event'


class Message:
    def __init__(self, msg_type, user_id, self_user_id, content=None, event=None):
        self.msg_type = msg_type
        self.user_id = user_id
        self.self_user_id = self_user_id
        self.content = content
        self.event=event

    @staticmethod
    def parse_xml(data):
        xml = ElementTree.fromstring(data)
        msgtype = xml.find("MsgType").text
        userid = xml.find("FromUserName").text
        myid = xml.find("ToUserName").text
        message = None
        if msgtype == MsgType.TEXT.value:
            content = xml.find("Content").text
            message = Message(MsgType.TEXT, userid, myid, content=content)
        elif msgtype == MsgType.EVENT.value:
            event = xml.find("Event").text
            message = Message(MsgType.EVENT, userid, myid, event=event)

        return message
