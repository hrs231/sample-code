import logging


class Loggable(object):
    """ Generic Logging helper class """

    def __init__(self):
        self.logger_active = False
        self.logger = None

    def init_logging(self, logger_name):
        self.logger = logging.getLogger(logger_name)
        logfile = "logs/" + logger_name + ".log"
        hdlr = logging.FileHandler(logfile)
        hdlr.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s'))
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)
        self.logger.info("Invoked")
        self.logger_active = True

    def log_info(self, msg):
        if self.logger_active:
            self.logger.info(msg)

    def log_error(self, msg):
        if self.logger_active:
            self.logger.error(msg)
