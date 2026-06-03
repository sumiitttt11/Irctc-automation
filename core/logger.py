"""
Structured logger.
  • Console: colour-coded, human-readable
  • File:    logs/tatkal_YYYYMMDD_HHMMSS.log  (rotating, no colour)
"""
import logging
import sys
from datetime import datetime
from pathlib import Path

_LOG_DIR = Path("logs")
_LOG_DIR.mkdir(exist_ok=True)

_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
_LOG_FILE = _LOG_DIR / f"tatkal_{_TIMESTAMP}.log"

# ── formatters ──────────────────────────────────────────────────────────────

_FILE_FMT  = logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s",
                                datefmt="%H:%M:%S.%f"[:-3])

class _ColourFmt(logging.Formatter):
    _COLOURS = {
        logging.DEBUG:    "\033[90m",   # grey
        logging.INFO:     "\033[0m",    # default
        logging.WARNING:  "\033[33m",   # yellow
        logging.ERROR:    "\033[31m",   # red
        logging.CRITICAL: "\033[1;31m", # bold red
    }
    _RESET = "\033[0m"

    def format(self, record):
        colour = self._COLOURS.get(record.levelno, "")
        msg = super().format(record)
        return f"{colour}{msg}{self._RESET}"

_CONSOLE_FMT = _ColourFmt("%(asctime)s  %(levelname)-8s  %(message)s",
                           datefmt="%H:%M:%S")

# ── build logger ────────────────────────────────────────────────────────────

def get_logger(name: str = "tatkal") -> logging.Logger:
    log = logging.getLogger(name)
    if log.handlers:
        return log          # already configured

    log.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(_CONSOLE_FMT)

    fh = logging.FileHandler(_LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(_FILE_FMT)

    log.addHandler(ch)
    log.addHandler(fh)
    return log


log = get_logger()
