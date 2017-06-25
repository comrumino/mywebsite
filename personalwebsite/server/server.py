#!/usr/bin/env python2
''' module doc string '''
from __future__ import print_function
import tornado.ioloop
from personalwebsite import myweb
from personalwebsite.myweb.constants import DIR

__all__ = ['run']


def run():
    handlers = [(r"/(?:home/?)?", myweb.HomeHandler), 
                (r"/portfolio/?(.*)?", myweb.PortfolioHandler),
                (r"/about-me/?", myweb.AboutMeHandler),
                (r"/static/(.*)", myweb.StaticHandler)]

    settings = {"template_path": DIR['template'],
                "template_whitespace": "oneline",
                "static_path": DIR['static'],
                "static_url_prefix": "/static/"}

    app = tornado.web.Application(handlers, **settings)
    _port = 80
    _address = '127.0.0.1'
    app.listen(_port, address=_address)
    tornado.ioloop.IOLoop.current().start()
    

if __name__ == "__main__":
    run()
