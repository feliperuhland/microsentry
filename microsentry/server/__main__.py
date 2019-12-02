import tornado.ioloop
import tornado.options
from tornado.options import define, options

from microsentry.server import applications


define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="debug mode", type=bool)


tornado.options.parse_command_line()
application = applications.MicroSentryApplication()
application.listen(options.port)
tornado.ioloop.IOLoop.current().start()
