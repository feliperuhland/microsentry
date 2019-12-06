import tornado.web
from tornado.options import options

from microsentry import services
from microsentry.server import handlers


class MicroSentryApplication(tornado.web.Application):
    def __init__(self):
        self.event_service = services.EventService()
        handler_list = [
            (r"/api/(\d+)/store/?", handlers.StoreHandler),
        ]
        settings = dict(debug=options.debug, autoreload=options.debug)
        super().__init__(handler_list, **settings)
