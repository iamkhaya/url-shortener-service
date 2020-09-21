import logging
from typing import List

import requests

from url_shortener_service.adapters.bitly_adapter import BitlyAdapter
from url_shortener_service.clients.abstract_client import AbstractClient
from url_shortener_service.dtos.short_url_dto import ShortUrlDto
from url_shortener_service.dtos.short_url_metric_dto import ShortUrlMetricDto


class BitlyClient(AbstractClient):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.requests_session = requests.session()
        self.bitly_adapter = BitlyAdapter()

    def shorten_url(self, long_url: str) -> ShortUrlDto:
        """
        shorten a url using the bitly api

        Args:
            long_url: The long url to shorten

        Returns:
            short_url: A corresponding short url

        """
        self.logger.info("shortening long url: %s", long_url)

        bitly_shortening_url: str = "https://api-ssl.bitly.com/v4/bitlinks"
        data: dict = {"long_url": long_url, "domain": self.bitly_settings["domain"]}

        response = requests.post(bitly_shortening_url, headers=self.headers, json=data)
        response.raise_for_status()

        converted_response: ShortUrlDto = self.bitly_adapter.convert_get_bitlink_response(response.json())

        self.logger.info("long url: %s, bitly response: %s", long_url, converted_response.__dict__)
        return converted_response

    def get_short_url_click_metrics(self, short_url: str) -> List[ShortUrlMetricDto]:
        """get click metrics for bitly defined short url

        Args:
            short_url: the url whose metrics is wanted

        Returns:
            link_clicks: a list of the clicks for the past 24 hours

        """
        WINDOW_SIZE_IN_HOURS = 24  # probably want this to be part of the parameters

        params = (
            ("unit", "hour"),
            ("units", WINDOW_SIZE_IN_HOURS),
            ("size", "5"),
        )

        url = "https://api-ssl.bitly.com/v4/bitlinks/" + short_url + "/clicks"

        response = requests.get(url=url, headers=self.headers, params=params)  # type: ignore
        response.raise_for_status()

        converted_response: List[ShortUrlMetricDto] = self.bitly_adapter.convert_get_bitlink_metrics_response(
            response.json()
        )
        return converted_response
