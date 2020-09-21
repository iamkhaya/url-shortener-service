import logging
from typing import Dict, List

from url_shortener_service.clients.bitly_client import BitlyClient
from url_shortener_service.controllers.abstract_controller import AbstractController
from url_shortener_service.dtos.short_url_dto import ShortUrlDto
from url_shortener_service.dtos.short_url_metric_dto import ShortUrlMetricDto


class UrlShortenerController(AbstractController):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.bitly_client = BitlyClient()

    def shorten_url(self, long_url: str) -> ShortUrlDto:
        """shorten the user given url

        Args:
            long_url: a long url

        Returns:
            short_url: A corresponding short url

        """
        short_url_dto: ShortUrlDto = self.bitly_client.shorten_url(long_url=long_url)
        return short_url_dto

    def get_short_url_click_metrics(self, short_url: str) -> List[ShortUrlMetricDto]:
        """get click metrics for bitly defined short url

        Args:
            short_url: the url whose metrics is wanted

        Returns:
            link_clicks: a list of the clicks for the past 30 days

        """
        response: List[ShortUrlMetricDto] = self.bitly_client.get_short_url_click_metrics(short_url=short_url)
        return response

    def shorten_urls(self, long_urls: List[str]) -> List[Dict]:
        """shorten a list of urls

        Args:
            long_urls: a list of long urls to be shortened

        Returns:
            shortened_urls: a list of dicts of the long urls and their corresponding short urls
        """

        shortened_urls = []
        for long_url in long_urls:
            short_url_dto: ShortUrlDto = self.bitly_client.shorten_url(long_url=long_url)

            shortened_urls.append({"long_url": long_url, "short_url": short_url_dto.link})

        return shortened_urls
