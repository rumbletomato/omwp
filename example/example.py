from waitress import serve

from globals import RequestInfo
from omwp import OMWPApplication
from services.results import OMWPHandlerResult200

omwp = OMWPApplication()


@omwp.route('/')
def index():
    return OMWPHandlerResult200("Hello, Stranger! This is index page!")


@omwp.route('/hello/<username>')
def hello():
    request_info = RequestInfo.get_instance()
    username = request_info.params.get('username', 'Stranger')
    return OMWPHandlerResult200(f"Hello, {username}! This is your personal page")


if __name__ == '__main__':
    serve(omwp, listen="0.0.0.0:8080")
