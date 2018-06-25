from __future__ import absolute_import
from __future__ import print_function
import tornado.ioloop
from .cfg import SETTINGS, PORT, ADDRESS
from .Handlers import HANDLERS


def main():
    _app = tornado.web.Application(HANDLERS, **SETTINGS)
    _app.listen(PORT, address=ADDRESS)
    tornado.ioloop.IOLoop.current().start()
