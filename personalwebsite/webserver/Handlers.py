"""Module for handlers"""
from __future__ import absolute_import
from __future__ import print_function
import hashlib
import tornado.web
import deveta
from .cfg import CONTENT, DIR, EXT, HOST

__all__ = ["StaticHandler", "HomeHandler", "PortfolioHandler", "AboutMeHandler", "HANDLERS"]


def _get_content_type(path):
    _match = EXT.search(path)
    if _match:
        return CONTENT[_match.group(1)]
    else:
        # Generally, default behavior would be an octet-stream but the auto-download behavior
        # is not desired. So let the default behavior be plain/text
        return CONTENT['text']


class StaticHandler(tornado.web.StaticFileHandler):
    """StaticFileHandler w/ extra headers"""
    def set_extra_headers(self, path):
        etags = ("js/app", "css/app", "partial")
        if path.startswith(etags):
            # For static assets, set client cacheable and max-age of one week 
            self.set_header("Cache-Control", "private,max-age=604800,must-revalidate") #one week
        else:
            # For public assets, prevent caching
            self.set_header("Cache-Control", "no-cache,no-store,must-revalidate")
            self.set_header("Content-Type", "text/plain")
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
        _files = deveta.locate.files(DIR[dir_key]) # The list returned is sorted, number files if a certain order is desired
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


HANDLERS = [(r"/?(?:home/?)?", HomeHandler),
            (r"/portfolio/?(.*)?", PortfolioHandler),
            (r"/about-me/?", AboutMeHandler),
            (r"/static/(.*)", StaticHandler),
            (r"/public/(.*)", StaticHandler, {"path": DIR['public']})]
