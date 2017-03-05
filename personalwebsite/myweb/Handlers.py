#!/usr/bin/env python2
from __future__ import print_function
import tornado.web
import deveta
from constants import *

__all__ =  ['StaticHandler', 'HomeHandler', 'BlogHandler', 'PortfolioHandler', 'ContactHandler']


class StaticHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        etags = ("js/app", "css/app", "partial")
        if path.startswith(etags):
            self.set_header("Cache-Control", "private,max-age=604800,must-revalidate") #One week
        else:
            self.set_header("Cache-Control", "private,max-age=3156000")
        self.set_header("X-Frame-Options", "deny")
        self.set_header("X-XSS-Protection", "1; mode=block")
        self.set_header("X-Content-Type-Options", "nosniff")

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        _partials = deveta.locate.files(DIR['partial'])
        _partials = map(lambda x: 'static/partial/'+x.split('/')[-1], _partials)
        _css_files = deveta.locate.files(DIR['css'])
        _css_files = map(lambda x: 'static/css/'+x.split('/')[-1], _css_files)
        self.render('index.html', partials=_partials, css_files=_css_files)

class BlogHandler(tornado.web.RequestHandler):
    def get(self, *args):
        self.write("BlogHandler")

class PortfolioHandler(tornado.web.RequestHandler):
    def get(self, *args):
        self.write("PortfolioHandler")

class ContactHandler(tornado.web.RequestHandler):
    def get(self, *args):
        self.write("ContactHandler")

if __name__ == "__main__":
    _partials = deveta.locate.files(DIR['partial'])
    _partials = map(lambda x: x.split('/')[-1], _partials)
    print(_partials)
