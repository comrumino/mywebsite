#!/usr/bin/env python2
''' module doc string '''
from __future__ import print_function
import tornado.ioloop
import myweb
from myweb.constants import DIR


if __name__ == "__main__":
    handlers = [(r"/(?:home/?)?", myweb.HomeHandler), 
                (r"/blog/(.*)?", myweb.BlogHandler), 
                (r"/portfolio/?(.*)?", myweb.PortfolioHandler),
                (r"/contact/?", myweb.ContactHandler),
                (r"/static/(.*)", myweb.StaticHandler)]

    settings = {"template_path": DIR['template'],
                "static_path": DIR['static'],
                "static_url_prefix": "/static/"}

    app = tornado.web.Application(handlers, **settings)
    _port = 80
    _address = '127.0.0.1'
    app.listen(_port, address=_address)
    tornado.ioloop.IOLoop.current().start()
