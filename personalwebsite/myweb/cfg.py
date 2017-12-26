"""Defines the constants to be used. Some constants are defined based on hostname."""
from __future__ import absolute_import
from __future__ import print_function
import socket
import deveta

__all__ = ["ADDRESS", "DIR", "HOST", "PORT", "SETTINGS"]


ADDRESS = "127.0.0.1"
DIR = {}
DIR["assets"] = "/".join([deveta.locate.parent_dir(), "assets"])
DIR["template"] = "/".join([DIR["assets"], "template"])
DIR["static"] = "/".join([DIR["assets"], "static"])
DIR["tmp"] = "/".join([DIR["static"], "tmp"])
DIR["partial"] = "/".join([DIR["static"], "partial"])
DIR["css"] = "/".join([DIR["static"], "css"])
DIR["js"] = "/".join([DIR["static"], "js"])
HOST = "stro.nz" if socket.gethostname() == "zestronza" else "127.0.0.1:8080"
PORT = 80 if socket.gethostname() == "zestronza" else 8080
SETTINGS = {}
SETTINGS["template_path"] = DIR["template"]
SETTINGS["template_whitespace"] = "oneline"
SETTINGS["static_path"] = DIR["static"]
SETTINGS["static_url_prefix"] = "/static/"
