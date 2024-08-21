"""e108"""

import logging, sys
logger: logging.Logger = logging.getLogger(__name__)

try:
    import asyncio
    import os
    import uvicorn
    from . import __description__, __version__, log_level, api, web
    logger.critical(f"""Iniciando {__name__} v{__version__}:\
{__description__} como módulo""")
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == "api":
                uvicorn.run(
                    api.app,
                    uds = os.getenv('API_SOCKET',
                        default = 'uvicorn.api.socket'),
                    log_level = log_level.lower(),
                )
            elif sys.argv[1] == "web":
                uvicorn.run(
                    web.app,
                    uds = os.getenv(
                    'WEB_SOCKET'.upper(),
                    default = 'uvicorn.web.socket',
                    ),
                    log_level = log_level.lower(),
                )
            else:
                logger.info("Só tem api ou web")
        else:
            logger.info("Só tem api ou web")
    except (OSError, NotImplementedError, asyncio.exceptions.CancelledError):
        logger.warning("""Sistema operacional sem suporte pra unix sockets, \
se for Windows pode ignorar esse aviso. Para parar de mostrar estes avisos, \
faça o seguinte:\
\nnão tem como!""")
        try:
            if len(sys.argv) > 1:
                if sys.argv[1] == "api":
                    uvicorn.run(
                        api.app,
                        host = os.getenv('API_HOST', default = '127.0.0.1'),
                        port = int(os.getenv('API_PORT', default = 8001)),
                        log_level = log_level.lower(),
                    )
                elif sys.argv[1] == "web":
                    uvicorn.run(
                        web.app,
                        host = os.getenv('WEB_HOST', default = '127.0.0.1'),
                        port = int(os.getenv('WEB_PORT', default = 8000)),
                        log_level = log_level.lower(),
                    )
                else:
                    logger.info("Só tem api ou web")
            else:
                logger.info("Só tem api ou web")
        except Exception as e1:
            logger.exception(e1)
    except Exception as e:
        logger.exception(e)
except Exception as e:
    logger.exception(e)
    sys.exit("Erro fatal, stacktrace acima")

logger.critical("Tchau")
