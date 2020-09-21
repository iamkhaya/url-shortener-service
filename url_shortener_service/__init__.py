import logging

from pyramid.config import Configurator


def main(global_config, **settings):  # pylint: disable=unused-argument
    """This function returns a Pyramid WSGI application.
    """

    with Configurator(settings=settings) as config:
        # handle cors
        config.include("url_shortener_service.modules.cors")
        # make sure to add this before other routes to intercept OPTIONS
        config.add_cors_preflight_handler()
        logging.info("logging routes")
        config.scan()
    return config.make_wsgi_app()
