"""
Utility tweens
Tweens are a Pyramid concept.
They are almost like middleware, but within the app itself.
Like wrappers around handlers, but without having to wrap the handlers
explicitly in decorators.
This module is for general tweens, you can write your own tweens within your own project.
"""
import datetime
import logging
import os

from pyramid.interfaces import IRoutesMapper

from .util import remove_none_from_dict


class remove_none_from_dict_tween(object):
    """
    A tween for removing Nones from Pyramid Response json
    """

    def __init__(self, handler, registry):
        self.handler = handler
        self.registry = registry

    def __call__(self, request):
        response = self.handler(request)
        if response.headers.get("Content-Type") == "application/json":
            response.json = remove_none_from_dict(response.json)
        return response


class handler_stats(object):
    """
    A tween for capturing handler metrics.
    """

    def __init__(self, handler, registry):
        self.handler = handler
        self.registry = registry
        self.service_name = registry.settings.get("service_name")

    def __call__(self, request):
        routes_mapper = self.registry.queryUtility(IRoutesMapper)
        matched_route = routes_mapper(request)["route"]
        route_name = matched_route.name if matched_route is not None else "unmatched_route"
        timer = None
        if self.stats_client:
            timer = self.stats_client.timer(route_name)
            timer.start()
        time_start = datetime.datetime.now()
        response = self.handler(request)
        time_elapsed = datetime.datetime.now() - time_start
        if os.environ.get("ROLE") == "DEV":
            logging.debug("%s response time: %s", route_name, time_elapsed)

        return response
