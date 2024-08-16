"""e108"""

import asyncio
import logging
logger: logging.Logger = logging.getLogger(__name__)

from . import __description__, __version__, log_level, web

logger.critical(f"""Iniciando {__name__} v{__version__}: {__description__} \
como módulo""")

try:
    import uvicorn
    try:
        uvicorn.run(
            web.app,
            uds = os.getenv(
            'WEB_SOCKET'.upper(),
            default = 'uvicorn.web.socket',
            ),
            # ~ forwarded_allow_ips = True,
            log_level = log_level.lower(),
            # ~ proxy_headers = True,
            # ~ reload = True,
            # ~ timeout_keep_alive = 1,
        )
    except (OSError, NotImplementedError, asyncio.exceptions.CancelledError):
        logger.warning("""Sistema operacional sem suporte pra unix sockets, \
se for Windows pode ignorar esse aviso. Para parar de mostrar estes avisos, \
faça o seguinte:\
\nnão tem como!""")
        uvicorn.run(
            web.app,
            host = os.getenv('WEB_HOST'.upper(), default = '127.0.0.1'),
            port = os.getenv('WEB_PORT'.upper(), default = 8000),
            # ~ forwarded_allow_ips = True,
            log_level = log_level.lower(),
            # ~ proxy_headers = True,
            # ~ reload = True,
            # ~ timeout_keep_alive = 1,
        )
except Exception as e:
    logger.exception(e)

logger.critical("Tchau")
