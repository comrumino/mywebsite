import hashlib
import os
import tornado.ioloop
import tornado.web
from . import logger, cfg

__all__ = ['main']


def _get_content_type(path):
    # Generally, default behavior would be an octet-stream but the auto-download behavior
    # is not desired. So let the default behavior be plain/text
    content_type = cfg.CONTENT['fallback']
    didx = path.rfind('.')
    if didx != -1:
        content_type = cfg.CONTENT.get(path[didx + 1:], content_type)
    return content_type


class StaticHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        etags = ("js/app", "css/app", "partial")
        if path.startswith(etags):
            # For static assets, set client cacheable and max-age of one week
            self.set_header("Cache-Control", "private,max-age=604800,must-revalidate")  # one week
        else:
            # For public assets, prevent caching
            self.set_header("Cache-Control", "no-cache,no-store,must-revalidate")
            content_type = _get_content_type(path)
            self.set_header("Content-Type", content_type)
        # self.set_header("X-Frame-Options", "deny")
        self.set_header("X-XSS-Protection", "1; mode=block")
        self.set_header("X-Content-Type-Options", "nosniff")


class XNStaticHandler(StaticHandler):

    def _get_mime_type(self, path):
        """ allows users to define mime type or returns fallback """
        try:
            content_type = None
            content_type_path = self.root.joinpath(f'{path}-type')
            if content_type_path.exists():
                with content_type_path.open() as fhandle:
                    _ext = fhandle.read().strip()
                content_type = cfg.CONTENT.get(_ext)
            if content_type is None:  # invalid value found or file not found at all
                content_type = cfg.CONTENT['fallback']
                logger.debug(f"Using fallback mime type of {content_type} for {path}")
        except Exception:
            logger.exception("Failed to get mime type")
        finally:
            return content_type

    def set_extra_headers(self, path):
        self.set_header("Content-Type", self._get_mime_type(path))
        self.set_header("Cache-Control", "no-cache,no-store,must-revalidate")

    def parse_url_path(self, url_path):
        fs_path = self.root.joinpath(url_path or "")  # when url doesn't end with /, url_path is None
        if fs_path == self.root:
            fs_path = fs_path.joinpath('xn_mime_fallback')
            logger.debug(f"XNStaticHandler is using path fallback {fs_path}")
        return fs_path


class BaseHandler(tornado.web.RequestHandler):
    """Initialize hrefs and use the file hash for each files version"""

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self._partials = BaseHandler._get_hrefs("partial")
        self._css_files = BaseHandler._get_hrefs("css")
        self._js_files = BaseHandler._get_hrefs("js")

    @staticmethod
    def _get_file_hash(dir_key, fname):
        """Returns sha224 hash of file for cache busting purposes"""
        fabspath = os.path.join(cfg.DIR[dir_key], fname)
        content_codec = 'utf-8'
        with open(fabspath, "r", encoding=content_codec, errors='surrogatereplace') as fhandle:
            file_content = fhandle.read()
            fhash = hashlib.sha224(file_content.encode('utf-8')).hexdigest()
        return fhash

    @staticmethod
    def _get_hrefs(dir_key, order=None):
        hrefs = []
        flist = sorted(os.listdir(cfg.DIR[dir_key]))
        for fname in flist:
            fhash = BaseHandler._get_file_hash(dir_key, fname)
            href = "//{}/static/{}/{}?v={}".format(cfg.HOST, dir_key, fname, fhash)
            hrefs.append(href)
        return hrefs

    def get_base_render_kwargs(self):
        base_render_kwargs = {"partials": self._partials,
                              "css_files": self._css_files,
                              "js_files": self._js_files,
                              "YEAR_STARTED": cfg.YEAR_STARTED}
        return base_render_kwargs


class HomeHandler(BaseHandler):
    def get(self, *args):
        home_render_kwargs = self.get_base_render_kwargs()
        self.render("index.html", **home_render_kwargs)


class PortfolioHandler(BaseHandler):
    def get(self, *args):
        portfolio_render_kwargs = self.get_base_render_kwargs()
        self.render("index.html", **portfolio_render_kwargs)


class AboutMeHandler(BaseHandler):
    def get(self, *args):
        aboutme_render_kwargs = self.get_base_render_kwargs()
        self.render("index.html", **aboutme_render_kwargs)


def main():
    handlers = [(r"/?(?:home/?)?", HomeHandler),
                (r"/portfolio/?(.*)?", PortfolioHandler),
                (r"/about-me/?", AboutMeHandler),
                (r"/static/(.*)", StaticHandler),
                (r"/xn--jea.cc(?:/(.*))?", XNStaticHandler, {"path": cfg.DIR['xnjeacc']}),
                (r"/public/(.*)", StaticHandler, {"path": cfg.DIR['public']})]
    logger.info("Starting main IO loop at {}:{}".format(cfg.ADDRESS, cfg.PORT))
    _app = tornado.web.Application(handlers, **cfg.SETTINGS)
    _app.listen(cfg.PORT, address=cfg.ADDRESS)
    tornado.ioloop.IOLoop.current().start()
