import logging
from systemd.journal import JournalHandler
from . import cfg

__all__ = ['logger']

logger = logging.getLogger(cfg.PKGNAME)
logger.setLevel(logging.DEBUG if cfg.DEBUG else logging.INFO)
logger.addHandler(JournalHandler(SYSLOG_IDENTIFIER=cfg.PKGNAME))
