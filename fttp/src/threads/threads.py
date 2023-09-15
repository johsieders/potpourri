## versuche mit threads
## js 2.8.04

from logging import getLogger
from threading import Condition, Thread
from time import sleep

logger = getLogger()


def callAsync(f, args):
    t = Thread(target=f, args=args)
    t.start()


class Buffer(object):
    def __init__(self, size):
        self.size = size
        self.items = 0
        self.sizeleft = size
        self.condition = Condition()

    def getSize(self):
        return self.size

    def getItem(self):
        self.condition.acquire()
        while self.items <= 0:
            self.condition.wait()
        self.items -= 1
        self.sizeleft += 1
        logger.info('getItem %3i %3i %3i' % (self.items, self.sizeleft, self.size))
        self.condition.notifyAll()
        self.condition.release()

    def putItem(self):
        self.condition.acquire()
        while self.sizeleft <= 0:
            self.condition.wait()
        self.items += 1
        self.sizeleft -= 1
        logger.info('putItem %3i %3i %3i' % (self.items, self.sizeleft, self.size))
        self.condition.notifyAll()
        self.condition.release()


class Actor(object):
    def __init__(self, action, rest, carryon):
        self.action = action
        self.rest = rest
        self.carryon = carryon

    def __call__(self):
        while self.carryon.isSet():
            sleep(self.rest)
            self.action()
