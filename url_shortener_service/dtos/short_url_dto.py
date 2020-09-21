from dataclasses import dataclass


@dataclass
class ShortUrlDto(object):
    short_url_id: str = ""
    short_url: str = ""
    link: str = ""
