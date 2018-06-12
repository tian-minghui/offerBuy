from django.test import TestCase

# Create your tests here.
from enum import Enum


class MsgType(Enum):
    TEXT = 'text'
    EVENT = 'event'

print(MsgType.TEXT)

