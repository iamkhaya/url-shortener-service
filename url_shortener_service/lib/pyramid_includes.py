"""
Includes for pyramid applications
"""
import json
import logging
import os
from collections import OrderedDict

import pyramid.httpexceptions
import pyramid_swagger.exceptions
import yaml
import yaml.resolver

logger = logging.getLogger(__name__)


def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    """
    This is to preserve ordering in the swagger definitions, which is important in the
    add_swagger_yaml_routing function.
    """

    class OrderedLoader(Loader):
        pass

    def include(loader, node):
        if isinstance(node, yaml.ScalarNode):
            return extract_file(loader.construct_scalar(node))
        elif isinstance(node, yaml.SequenceNode):
            result = []
            for filename in loader.construct_sequence(node):
                result += extract_file(filename)
            return result
        elif isinstance(node, yaml.MappingNode):
            result = {}
            for k, v in loader.construct_mapping(node).items():
                result[k] = extract_file(v)
            return result
        else:
            raise yaml.constructor.ConstructorError

    def extract_file(filename):
        file_path = os.path.join(_root, filename)
        with open(file_path, "r") as f:
            return yaml.load(f, OrderedLoader)

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    _root = os.path.split(stream.name)[0]

    OrderedLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)

    # Add tags to be recognised as constructors in yaml
    OrderedLoader.add_constructor("!include", include)
    OrderedLoader.add_constructor("!import", include)

    return yaml.load(stream, OrderedLoader)


def add_swagger_yaml_routing(config):
    """
    Load the swagger yaml file, and wire up the handlers and routes.
    """
    settings = config.registry.settings
    yaml_path = os.path.join(
        settings["pyramid_swagger.schema_directory"],
        settings["pyramid_swagger.schema_file"],
    )

    if os.path.isfile(yaml_path):
        with open(yaml_path) as yaml_file:
            swagger_dict = ordered_load(yaml_file, yaml.SafeLoader)
            settings["swagger_dict"] = swagger_dict

        for path, methods in swagger_dict["paths"].items():
            for method, action in methods.items():
                config.add_route(action["operationId"], path, request_method=method.upper())
                logger.info(
                    "Added route: %s for path: %s for method: %s",
                    action["operationId"],
                    path,
                    method.upper(),
                )
    else:
        raise Exception("Swagger file not found at %s" % os.path.abspath(yaml_path))


def swagger_yaml_to_json(config):
    """
    Parse a yaml file, and write it out to a json file.
    Pyramid_swagger only supports json at this point.
    Ordering is preserved during the conversion.
    """
    settings = config.registry.settings
    yaml_path = os.path.join(
        settings["pyramid_swagger.schema_directory"],
        settings["pyramid_swagger.yaml_file"],
    )

    json_path = os.path.join(
        settings["pyramid_swagger.schema_directory"],
        settings["pyramid_swagger.json_file"],
    )

    if os.path.isfile(yaml_path):
        with open(yaml_path) as yaml_file:
            swagger_yaml = ordered_load(yaml_file, yaml.SafeLoader)

        with open(json_path, "w+") as json_file:
            json.dump(swagger_yaml, json_file, indent=2)

        settings["swagger_dict"] = swagger_yaml
    elif not os.path.isfile(json_path):
        raise Exception("Swagger file not found at %s" % os.path.abspath(json_path))


# View definitions for handling exceptions
def server_error(exc, request):
    """
    Catchall exception handler
    """
    status = exc.status_int if hasattr(exc, "status_int") else 500

    # since this is an unhandled error that not caught by concrete rest service, we don't want to send
    # the full stack trace back to caller, as it might appear on end customer's cellphone.
    # But we do need to log the exception
    logger.info("error on url: %s", request.url)
    logger.info("request params: %s", request.params)
    logger.exception(exc)
    error_dict = {
        "message": exc.message,
        "status": status,
    }
    response = pyramid.response.Response(json.dumps(error_dict))
    response.status_int = status
    if error_dict and isinstance(error_dict, dict):
        response.content_type = "application/json"
    return response


def error_handling(config):
    """
    Wire up exceptions to the server_error handler.
    This is mostly as an example, you can do what you want here.
    """
    config.add_view(server_error, context=pyramid_swagger.exceptions.RequestValidationError)

    config.add_view(server_error, context=pyramid_swagger.exceptions.ResponseValidationError)

    config.add_view(server_error, context=pyramid.httpexceptions.HTTPException)
    config.add_view(server_error, context=Exception)
