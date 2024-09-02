"""hobrsite"""

import locale, logging, os, sys

log_level: str = os.getenv('LOG_LEVEL'.upper(), default = logging.INFO)
logging.basicConfig(level = log_level)
logger: logging.Logger = logging.getLogger(__name__)

locale.setlocale(locale.LC_NUMERIC, "pt_BR.UTF8")

from ._version import __version__

__name__: str = "hobrsite"
__description__: str = "Mais um projeto sem futuro"

logger.critical(f"Iniciando {__name__} v{__version__}: {__description__}")
