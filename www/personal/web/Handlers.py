#!/usr/bin/env python2
from __future__ import print_function
__all__ =  ['StaticHandler', 'HomeHandler', 'BlogHandler', 'PortfolioHandler', 'ContactHandler']
import tornado.web

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
        self.render('index.html', entries=[])

class BlogHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("BlogHandler")

class PortfolioHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("PortfolioHandler")

class ContactHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("ContactHandler")
