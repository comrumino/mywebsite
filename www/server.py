#!/usr/bin/env python2
from __future__ import print_function
import tornado.ioloop
import personal.web


if __name__ == "__main__":
    handlers = [(r"/(?:home/?)?", personal.web.HomeHandler), 
                (r"/blog/(.*)?", personal.web.BlogHandler), 
                (r"/portfolio/?(.*)?", personal.web.PortfolioHandler),
                (r"/contact/?", personal.web.ContactHandler),
                (r"/static/(.*)", personal.web.StaticHandler)]
    settings = {"template_path": "/data/www/personal/template",
                "static_path": "/data/www/personal/static",
                "static_url_prefix": "/static/"}
    app = tornado.web.Application(handlers, **settings)
    _port = 80
    _address = '127.0.0.1'
    app.listen(_port, address=_address)
    tornado.ioloop.IOLoop.current().start()
