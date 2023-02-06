import logging


class Logger:
    def __int__(self):
        FORMAT = '%(asctime)s | %(funcName)s | %(message)s'
        logging.basicConfig(format=FORMAT, level=10, filename='./logs.log')
        self.logger = logging.getLogger('api')
        self.logger.setLevel(10)

    def write(self, msg):
        self.logger.debug(msg)


logger = Logger()
