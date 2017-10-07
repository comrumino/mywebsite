#!/usr/bin/env python2
"""Entry point for personalwebsite"""
from __future__ import print_function
import tornado.ioloop
from myweb.constants import HANDLERS, SETTINGS, PORT, ADDRESS


if __name__ == "__main__":
    _app = tornado.web.Application(HANDLERS, **SETTINGS)
    _app.listen(PORT, address=ADDRESS)
    tornado.ioloop.IOLoop.current().start()
