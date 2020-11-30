"""cfg, a module for global configurations
    HOST, will use hostname if it is a registered domain, otherwise 127.0.0.1:8080
"""
import datetime
from pathlib import Path
import socket
import tldextract
from .. import PKGNAME

__all__ = ["YEAR_STARTED", "ADDRESS", "CONTENT", "DIR", "HOST", "PORT", "SETTINGS", "PKGNAME", "DEBUG"]


YEAR_STARTED = datetime.date.today().strftime('%Y')
ADDRESS = "127.0.0.1"
CONTENT = {}
CONTENT['7z'] = 'application/x-7z-compressed'
CONTENT['ai'] = 'application/postscript'
CONTENT['asm'] = 'text/x-asm'
CONTENT['bmp'] = 'image/bmp'
CONTENT['bz2'] = 'application/x-bzip2'
CONTENT['bz'] = 'application/x-bzip'
CONTENT['cc'] = 'text/x-c'
CONTENT['cpp'] = 'text/x-c'
CONTENT['csv'] = 'text/csv'
CONTENT['c'] = 'text/x-c'
CONTENT['cxx'] = 'text/x-c'
CONTENT['dic'] = 'text/x-c'
CONTENT['eps'] = 'application/postscript'
CONTENT['for'] = 'text/x-fortran'
CONTENT['f'] = 'text/x-fortran'
CONTENT['gif'] = 'image/gif'
CONTENT['js'] = 'text/javascript'
CONTENT['gtar'] = 'application/x-gtar'
CONTENT['gz'] = 'application/gzip'
CONTENT['hh'] = 'text/x-c'
CONTENT['h'] = 'text/x-c'
CONTENT['html'] = 'text/html'
CONTENT['ico'] = 'image/x-icon'
CONTENT['java'] = 'text/x-java-source'
CONTENT['jpeg'] = 'image/jpeg'
CONTENT['jpe'] = 'image/jpeg'
CONTENT['jpg'] = 'image/jpeg'
CONTENT['pas'] = 'text/x-pascal'
CONTENT['pdf'] = 'application/pdf'
CONTENT['png'] = 'image/png'
CONTENT['ps'] = 'application/postscript'
CONTENT['p'] = 'text/x-pascal'
CONTENT['s'] = 'text/x-asm'
CONTENT['svg'] = 'image/svg+xml'
CONTENT['svgz'] = 'image/svg+xml'
CONTENT['tar'] = 'application/x-tar'
CONTENT['tar.bz2'] = 'application/x-gtar'
CONTENT['tar.gz'] = 'application/x-gtar'
CONTENT['tar.lzma'] = 'application/x-gtar'
CONTENT['tar.xz'] = 'application/x-gtar'
CONTENT['tar.Z'] = 'application/x-gtar'
CONTENT['tbz2'] = 'application/x-gtar'
CONTENT['text'] = 'text/plain'
CONTENT['tgz'] = 'application/x-gtar'
CONTENT['tlz'] = 'application/x-gtar'
CONTENT['txt'] = 'text/plain'
CONTENT['txz'] = 'application/x-gtar'
CONTENT['zip'] = 'application/zip'
CONTENT['fallback'] = CONTENT['txt']
DEBUG = False
DIR = {}
DIR["base"] = Path(__file__).resolve().parent.parent
DIR["assets"] = DIR["base"].joinpath("assets")
DIR["template"] = DIR["assets"].joinpath("template")
DIR["static"] = DIR["assets"].joinpath("static")
DIR["public"] = Path("/data/www/public")
DIR["xnjeacc"] = Path("/data/www/xnjeacc")
DIR["tmp"] = DIR["static"].joinpath("tmp")
DIR["partial"] = DIR["static"].joinpath("partial")
DIR["css"] = DIR["static"].joinpath("css")
DIR["js"] = DIR["static"].joinpath("js")
_hostname_tld = tldextract.extract(socket.gethostname())
HOST = "127.0.0.1:9001"
if _hostname_tld.registered_domain:
    HOST = _hostname_tld.registered_domain
else:
    DEBUG = True
PORT = 9001
SETTINGS = {}
SETTINGS["template_path"] = DIR["template"]
SETTINGS["template_whitespace"] = "oneline"
SETTINGS["static_path"] = DIR["static"]
SETTINGS["static_url_prefix"] = "/static/"
