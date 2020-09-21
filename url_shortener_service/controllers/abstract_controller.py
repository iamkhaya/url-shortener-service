import abc

from url_shortener_service.config.config import Config


class AbstractController(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.config = Config()
