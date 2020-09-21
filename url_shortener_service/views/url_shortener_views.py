import csv
import logging
from typing import List

import requests
from pyramid.response import FileResponse
from pyramid.view import view_config

from url_shortener_service.controllers.url_shortener_controller import UrlShortenerController
from url_shortener_service.dtos.short_url_dto import ShortUrlDto
from url_shortener_service.dtos.short_url_metric_dto import ShortUrlMetricDto
from url_shortener_service.errors import APIException


@view_config(route_name="shorten_url", request_method="POST", renderer="json")
def shorten_url(request):
    """
    shorten a long url
    """
    long_url = request.swagger_data["long_url"]["long_url"]
    logging.info("**** long url: %s", long_url)
    url_shortener_controller = UrlShortenerController()

    try:
        response: ShortUrlDto = url_shortener_controller.shorten_url(long_url)
        return {"short_url_link": response.link}
    except requests.exceptions.HTTPError as e:
        logging.exception("An error occured while shortening url")
        raise APIException(message=e)
    except ValueError as e:
        logging.exception("Invalid data received from 3rd party service")
        raise APIException(message=e)


@view_config(route_name="get_short_url_click_metrics", request_method="GET", renderer="json")
def get_short_url_click_metrics(request):
    """
    get click metrics for a short url
    """
    short_url = request.swagger_data["short_url"]
    url_shortener_controller = UrlShortenerController()
    try:
        response: List[ShortUrlMetricDto] = url_shortener_controller.get_short_url_click_metrics(short_url)
        return [short_url_metric.__dict__ for short_url_metric in response]
    except requests.exceptions.HTTPError as e:
        logging.exception("An error occured while retrieving metrics")
        raise APIException(message=e)
    except ValueError as e:
        logging.exception("Invalid data received from 3rd party service")
        raise APIException(message=e)


@view_config(route_name="get_short_urls_from_file", request_method="POST")
def get_short_urls_from_file(request):
    """
    shorten_urls_from_file
    """
    url_shortener_controller = UrlShortenerController()

    # extract long_urls from file
    short_urls_file = request.swagger_data["short_urls_file"].read().decode("utf-8")

    reader = csv.reader(short_urls_file.split("\n"), delimiter=",")

    long_urls = []
    for long_url in reader:
        if long_url:
            long_urls.append(long_url[0])

    try:
        # shorten long urls
        shortened_urls = url_shortener_controller.shorten_urls(long_urls=long_urls)
    except requests.exceptions.HTTPError as e:
        logging.exception("An error occured while retrieving metrics")
        raise APIException(message=e)
    except ValueError as e:
        logging.exception("Invalid data received from 3rd party service")
        raise APIException(message=e)

    # write response file
    with open("output.csv", mode="w") as csv_file:
        fieldnames = ["long_url", "short_url"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for shortened_url in shortened_urls:
            writer.writerow(shortened_url)

    # build response
    response = FileResponse("output.csv")
    response.content_type = "text/csv"
    response.content_encoding = "utf-8"

    return response
