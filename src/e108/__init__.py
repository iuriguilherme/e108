"""e108"""

import logging
import os

log_level: str = os.getenv('LOG_LEVEL'.upper(), default = logging.INFO)
logging.basicConfig(level = log_level)
logger: logging.Logger = logging.getLogger(__name__)

from ._version import __version__

__name__: str = "e108"
__description__: str = "Mais um projeto sem futuro"

logger.critical(f"Iniciando {__name__} v{__version__}: {__description__}")
