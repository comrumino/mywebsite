"""Module for handlers"""
from __future__ import absolute_import
from __future__ import print_function
import hashlib
import tornado.web
import deveta
from .cfg import DIR, HOST

__all__ = ["StaticHandler", "HomeHandler", "PortfolioHandler", "AboutMeHandler", "HANDLERS"]


class StaticHandler(tornado.web.StaticFileHandler):
    """StaticFileHandler w/ extra headers"""
    def set_extra_headers(self, path):
        etags = ("js/app", "css/app", "partial")
        if path.startswith(etags):
            self.set_header("Cache-Control", "private,max-age=604800,must-revalidate") #one week
        else:
            self.set_header("Cache-Control", "private,max-age=3156000")
        self.set_header("X-Frame-Options", "deny")
        self.set_header("X-XSS-Protection", "1; mode=block")
        self.set_header("X-Content-Type-Options", "nosniff") 


class BaseHandler(tornado.web.RequestHandler):
    """Base class for the handlers to be defined and provides files to be rendered"""
    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self._partials = BaseHandler._get_files("partial")
        self._css_files = BaseHandler._get_files("css")
        self._js_files = BaseHandler._get_files("js")

    @staticmethod
    def _hash_file(filename):
        """Returns sha224 hash of file for cache busting purposes"""
        return hashlib.sha224(open(filename, "r").read()).hexdigest()

    @staticmethod
    def _get_fname_string(dir_key, fname):
        """Returns file name w/ version as result of hash_file()"""
        _host = HOST
        _fname = fname.split("/")[-1]
        _hash_file = BaseHandler._hash_file(fname)
        return "//{}/static/{}/{}?v={}".format(_host, dir_key, _fname, _hash_file)

    @staticmethod
    def _get_files(dir_key, order=None):
        """Returns a list of strings and is set in BaseHandler scope"""
        _files = deveta.locate.files(DIR[dir_key])
        return [BaseHandler._get_fname_string(dir_key, _fname) for _fname in _files if not _fname.split('/')[-1].startswith('.')]



class HomeHandler(BaseHandler):
    """Handler for the home tab"""
    def get(self, *args):
        """Responds to the HTTP GET request with rendered template for home"""
        home_render_kwargs = {"partials": self._partials,
                              "css_files": self._css_files,
                              "js_files": self._js_files}
        self.render("index.html", **home_render_kwargs)


class PortfolioHandler(BaseHandler):
    """Handler for the portfolio tab"""
    def get(self, *args):
        """Responds to the HTTP GET request with rendered template for portfolio"""
        portfolio_render_kwargs = {"partials": self._partials,
                                   "css_files": self._css_files,
                                   "js_files": self._js_files}
        self.render("index.html", **portfolio_render_kwargs)


class AboutMeHandler(BaseHandler):
    """Handler for the aboutme tab"""
    def get(self, *args):
        """Responds to the HTTP GET request with rendered template for aboutme"""
        aboutme_render_kwargs = {"partials": self._partials,
                                 "css_files": self._css_files,
                                 "js_files": self._js_files}
        self.render("index.html", **aboutme_render_kwargs)


HANDLERS = [(r"/(?:home/?)?", HomeHandler),
            (r"/portfolio/?(.*)?", PortfolioHandler),
            (r"/about-me/?", AboutMeHandler),
            (r"/static/(.*)", StaticHandler)]
