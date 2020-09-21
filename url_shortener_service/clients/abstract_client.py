import abc

from url_shortener_service.config.config import Config


class AbstractClient(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.config = Config()
        self.headers = {
            "Authorization": "Bearer c2c4d564a633fcc6151e6bc4dd27f0234761a3f2",
            "Content-Type": "application/json",
        }
