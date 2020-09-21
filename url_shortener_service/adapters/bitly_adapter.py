from typing import Dict

from url_shortener_service.dtos.short_url_dto import ShortUrlDto
from url_shortener_service.dtos.short_url_metric_dto import ShortUrlMetricDto


class BitlyAdapter:
    def convert_get_bitlink_response(self, response: Dict):
        """
        convert the get bitlink response to a business class dto
        """
        return ShortUrlDto(short_url_id=response["id"], short_url=response["link"], link=response["link"])

    def convert_get_bitlink_metrics_response(self, response: Dict):
        """
        convert the get bitlink metrics response to a business class dto
        """
        return [
            ShortUrlMetricDto(date=link_click["date"], number_of_clicks=link_click["clicks"])
            for link_click in response["link_clicks"]
        ]
