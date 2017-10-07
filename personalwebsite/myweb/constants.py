"""Module wherein constants are defined"""
from __future__ import print_function
import socket
import deveta
from Handlers import HomeHandler, PortfolioHandler, AboutMeHandler, StaticHandler

__all__ = ["DIR", "INFO", "HANDLERS", "SETTINGS", "PORT", "ADDRESS"]


DIR = {}
DIR["assets"] = "/".join([deveta.locate.parent_dir(), "assets"])
DIR["template"] = "/".join([DIR["assets"], "template"])
DIR["static"] = "/".join([DIR["assets"], "static"])
DIR["tmp"] = "/".join([DIR["static"], "tmp"])
DIR["partial"] = "/".join([DIR["static"], "partial"])
DIR["css"] = "/".join([DIR["static"], "css"])
DIR["js"] = "/".join([DIR["static"], "js"])

INFO = {}
INFO["host"] = "stro.nz" if socket.gethostname() == "zestronza" else "127.0.0.1"

HANDLERS = [(r"/(?:home/?)?", HomeHandler),
            (r"/portfolio/?(.*)?", PortfolioHandler),
            (r"/contact/?", AboutMeHandler),
            (r"/static/(.*)", StaticHandler)]
SETTINGS = {}
SETTINGS["template_path"] = DIR["template"]
SETTINGS["template_whitespace"] = "oneline"
SETTINGS["static_path"] = DIR["static"]
SETTINGS["static_url_prefix"] = "/static/"
PORT = 80
ADDRESS = "127.0.0.1"
