#!/usr/bin/env python2
from __future__ import print_function
import hashlib
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


def hash_file(filename):
    return hashlib.sha224(open(filename, 'r').read()).hexdigest()

def get_files(dir_key):
    files = deveta.locate.files(DIR[dir_key])
    return map(lambda x: '//{}/static/{}/{}?v={}'.format(INFO['host'], dir_key, x.split('/')[-1], hash_file(x)), files)

class BaseHandler(tornado.web.RequestHandler):
    my_partials = get_files('partial')
    my_css_files = get_files('css')
    my_js_files = get_files('js')

    def get_partials(self):
        return BaseHandler.my_partials

    def get_css_files(self):
        return BaseHandler.my_css_files

    def get_js_files(self):
        return BaseHandler.my_js_files
        

class HomeHandler(BaseHandler):
    def get(self, *args):
        home_render_kwargs = {'partials': self.get_partials(),
                              'css_files': self.get_css_files(),
                              'js_files': self.get_js_files()}
        self.render('index.html', **home_render_kwargs)


class BlogHandler(BaseHandler):
    def get(self, *args):
        blog_render_kwargs = {'partials': self.get_partials(),
                              'css_files': self.get_css_files(),
                              'js_files': self.get_js_files()}
        self.render('index.html', **blog_render_kwargs)

class PortfolioHandler(BaseHandler):
    def get(self, *args):
        portfolio_render_kwargs = {'partials': self.get_partials(),
                                   'css_files': self.get_css_files(),
                                   'js_files': self.get_js_files()}
        self.render('index.html', **portfolio_render_kwargs)

class ContactHandler(BaseHandler):
    def get(self, *args):
        contact_render_kwargs = {'partials': self.get_partials(),
                                 'css_files': self.get_css_files(),
                                 'js_files': self.get_js_files()}
        self.render('index.html', **contact_render_kwargs)

if __name__ == "__main__":
    _partials = deveta.locate.files(DIR['partial'])
    _partials = map(lambda x: x.split('/')[-1], _partials)
    print(_partials)
