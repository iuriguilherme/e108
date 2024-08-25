"""api"""

import logging, sys
logger: logging.Logger = logging.getLogger(__name__)

try:
    from fastapi import FastAPI
    from .v1 import um
    from .v2 import dois
except Exception as e:
    logger.exception(e)
    sys.exit("Erro fatal, stacktrace acima")

app: FastAPI = FastAPI()
app.include_router(um, prefix = "/api/v1")
app.include_router(dois, prefix = "/api/v2")
