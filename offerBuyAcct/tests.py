from django.test import TestCase

# Create your tests here.

import socket
#获取本机电脑名
myname = socket.getfqdn(socket.gethostname())
print(myname)
#获取本机ip
myaddr = socket.gethostbyname(myname)
print(myaddr)