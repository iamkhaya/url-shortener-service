# mypy: ignore-errors
import logging
import os
from typing import Dict

import getconf


class Config:

    _config = None  # type: ignore

    def __init__(self):
        try:
            ROLE = os.environ["ROLE"]
            logging.info("ROLE : %s", ROLE)
            config_file_name = "{}.ini".format(str(ROLE).lower())
            base_path = os.path.dirname(__file__)
            config_file = os.path.join(base_path, config_file_name)

            logging.info("loading configuration: %s %s", config_file_name, config_file)
            self._config = getconf.ConfigGetter(ROLE, [config_file])
        except KeyError:
            logging.exception("please set ROLE environment variable")
            raise

    def get_bitly_settings(self) -> Dict:
        """Get bitly setting"""
        logging.info("getting bitly settings")

        bitly_settings: Dict = {
            "domain": self._config.getstr("bitly.domain"),
            "api_key": self._config.getstr("bitly.api_key"),
        }

        return bitly_settings
