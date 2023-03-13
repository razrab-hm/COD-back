import logging


class Logger:
    FORMAT = '%(asctime)s | %(funcName)s | %(message)s'
    logging.basicConfig(format=FORMAT, level=10, filename='./logs/logs.log')
    logger = logging.getLogger('api')
    logger.setLevel(10)

    def input(self, *msg):
        self.logger.debug(msg='input: ' + str(msg))

    def output(self, *msg):
        self.logger.debug(msg='output: ' + str(msg))


log = Logger()
