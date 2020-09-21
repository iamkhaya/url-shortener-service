from dataclasses import dataclass


@dataclass
class ShortUrlMetricDto(object):
    date: str
    number_of_clicks: int
