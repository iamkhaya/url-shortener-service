import abc

from url_shortener_service.config.config import Config


class AbstractClient(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.config = Config()
        self.bitly_settings = self.config.get_bitly_settings()
        self.headers = {
            "Authorization": "Bearer {}".format(self.bitly_settings["api_key"]),
            "Content-Type": "application/json",
        }
