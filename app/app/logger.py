import logging

FORMAT = '%(asctime)s | %(funcName)s | %(message)s'
logging.basicConfig(format=FORMAT, level=10, filename='logs.log')

logger = logging.getLogger('api')
logger.setLevel(10)


def test(val):
    logger.debug(val)
    return val+1


test(5)
