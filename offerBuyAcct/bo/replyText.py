# -*- coding:utf-8 -*-
import time

WELCOME=''

class replyText:
    def __init__(self, userid, myid, content, timestamp=int(time.time())):
        self.userid = userid
        self.myid = myid
        self.content = content
        self.timestamp = timestamp

    def get_dict(self):
        return {
            "toUser": self.userid,
            "fromUser": self.myid,
            "createTime": self.timestamp,
            "content": self.content
        }
