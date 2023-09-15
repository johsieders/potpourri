## teste consumer/producer
## js 3.8.2004

import logging
import threading
import time
import unittest


class TestConsumerProducer(unittest.TestCase):
    def test(self):
        logger = logging.getLogger()
        f = logging.FileHandler("consumerproducer.txt", 'w')
        logger.addHandler(f)
        logger.setLevel(logging.INFO)

        carryon = threading.Event()
        carryon.set()

        buffer = Buffer(7)
        producers = [Thread(target=Actor(buffer.putItem, 0.01, carryon)) for i in range(10)]
        consumers = [Thread(target=Actor(buffer.getItem, 0.1, carryon)) for i in range(100)]
        for c in consumers:
            c.start()
        for p in producers:
            p.start()

        time.sleep(1)
        carryon.clear()
        f.flush()


def suite():
    return unittest.makeSuite(TestConsumerProducer)


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
