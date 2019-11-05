"""cfg, a module for global configurations
    HOST, will use hostname if it is a registered domain, otherwise 127.0.0.1:8080
    EXT, a compiled regular expression for identifying if the file extension is supported
        The original expression was
            _ext = r'.(?:7z|ai|eps|ps|bmp|bz|bz2|c|cc|cxx|cpp|h|hh|dic|csv|f|for|gif|gz|ico|java|'
            _ext += r'jpeg|jpg|jpe|pdf|png|p|pas|s|asm|svg|svgz|tar|tar.gz|tar.bz2|tar.xz|tar.Z|tar.lzma|'
            _ext += r'txz|tbz2|tgz|tlz|gtar|txt|text|conf|def|list|in|log|err|info|warn|crit|notice|'
            _ext += r'css|html|xml|zip)$'
        which is more human readable. Even so, the regex in use requires fewer steps to match.
"""
import datetime
import os
import re
import socket
from tldextract import TLDExtract
from .. import PKGNAME

__all__ = ["YEAR_STARTED", "ADDRESS", "CONTENT", "DIR", "EXT", "HOST", "PORT", "SETTINGS", "PKGNAME"]


_tld_extract = TLDExtract(cache_file=False)

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
CONTENT['conf'] = 'text/plain'
CONTENT['cpp'] = 'text/x-c'
CONTENT['crit'] = 'text/plain'
CONTENT['css'] = 'text/plain'
CONTENT['csv'] = 'text/csv'
CONTENT['c'] = 'text/x-c'
CONTENT['cxx'] = 'text/x-c'
CONTENT['def'] = 'text/plain'
CONTENT['dic'] = 'text/x-c'
CONTENT['eps'] = 'application/postscript'
CONTENT['err'] = 'text/plain'
CONTENT['for'] = 'text/x-fortran'
CONTENT['f'] = 'text/x-fortran'
CONTENT['gif'] = 'image/gif'
CONTENT['gtar'] = 'application/x-gtar'
CONTENT['gz'] = 'application/gzip'
CONTENT['hh'] = 'text/x-c'
CONTENT['h'] = 'text/x-c'
CONTENT['html'] = 'text/plain'
CONTENT['ico'] = 'image/x-icon'
CONTENT['info'] = 'text/plain'
CONTENT['in'] = 'text/plain'
CONTENT['java'] = 'text/x-java-source'
CONTENT['jpeg'] = 'image/jpeg'
CONTENT['jpe'] = 'image/jpeg'
CONTENT['jpg'] = 'image/jpeg'
CONTENT['list'] = 'text/plain'
CONTENT['log'] = 'text/plain'
CONTENT['notice'] = 'text/plain'
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
CONTENT['warn'] = 'text/plain'
CONTENT['xml'] = 'text/plain'
CONTENT['zip'] = 'application/zip'
DIR = {}
DIR["base"] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR["assets"] = "/".join([DIR["base"], "assets"])
DIR["template"] = "/".join([DIR["assets"], "template"])
DIR["static"] = "/".join([DIR["assets"], "static"])
DIR["public"] = "/data/www/public"
DIR["tmp"] = "/".join([DIR["static"], "tmp"])
DIR["partial"] = "/".join([DIR["static"], "partial"])
DIR["css"] = "/".join([DIR["static"], "css"])
DIR["js"] = "/".join([DIR["static"], "js"])
_ext = r'.(7z|a(?:i|sm)|e?ps|b(mp|z2?)|c(c|xx|pp|sv|ss|onf|rit)?|h(?:h?|tml)|'
_ext += r'd(?:ic|ef)|f(?:or)?|g(if|z|tar)|i(?:co|n(?:fo)?)|j(ava|pe?g?)|p(?:ng|as|df)?|'
_ext += r's(?:vgz?)?|t(?:e?xt|bz2|(?:x|g|l)z|ar(?:.(?:(?:x|g)z|bz2|Z|lzma))?)|'
_ext += r'l(?:ist|og)|err|warn|notice|xml|zip)$'
EXT = re.compile(r'{}'.format(_ext), flags=re.M)
_domain = _tld_extract(socket.gethostname()).registered_domain
HOST = _domain if _domain else "127.0.0.1:9001"
PORT = 9001
SETTINGS = {}
SETTINGS["template_path"] = DIR["template"]
SETTINGS["template_whitespace"] = "oneline"
SETTINGS["static_path"] = DIR["static"]
SETTINGS["static_url_prefix"] = "/static/"
