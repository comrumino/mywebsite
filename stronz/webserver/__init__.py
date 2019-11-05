import logging
from systemd.journal import JournalHandler
from . import cfg

__all__ = ['logger']


logging.getLogger().addHandler(JournalHandler(SYSLOG_IDENTIFIER=cfg.PKGNAME))
logger = logging.getLogger(cfg.PKGNAME)
logger.setLevel(logging.INFO)
