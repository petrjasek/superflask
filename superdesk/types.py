"""Plugin types definition."""

import flask

class PluginType(type):
    """Base Type for plugin base classes."""

    def __init__(cls, name, bases, attrs):
        """Registers class on init."""
        if cls.plugins is None:
            cls.plugins = []
        else:
            cls.plugins.append(cls)
        super(PluginType, cls).__init__(name, bases, attrs)

class Resource(object):
    """Base class for Resources."""

    __metaclass__ = PluginType

    plugins = None
    methods = ('GET', )

    def handle(self):
        """Handle request via calling respective method on resource."""
        method = flask.request.method.lower()
        response = flask.jsonify(getattr(self, method, noop)())
        response.status_code = 200
        return response

    def get_endpoint(self):
        """Get resource endpoint from attribute or lowercase name."""
        default_endpoint = '/%s/' % self.__class__.__name__.lower()
        return getattr(self, 'endpoint', default_endpoint)

def noop(*args, **kwargs):
    """Noop method used in case get/post/put/delete is not implemented."""
    return ""

def get_blueprint():
    """Get flask app blueprint."""
    blueprint = flask.Blueprint('api', __name__)
    for cls in Resource.plugins:
        resource = cls()
        blueprint.add_url_rule(resource.get_endpoint(),
                endpoint=cls.__name__.lower(),
                view_func=resource.handle,
                methods=resource.methods)
    return blueprint
