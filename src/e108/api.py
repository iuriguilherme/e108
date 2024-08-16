"""api"""

import logging
from fastapi import FastAPI

log_level: int = logging.INFO
logging.basicConfig(level = log_level)
logger: logging.Logger = logging.getLogger(__name__)

app: FastAPI = FastAPI()

@app.get("/")
async def index() -> dict:
    """GET /"""
    return {
        "status": True,
        "message": """Lista de endpoints:
GET /usuarios
GET /usuario/<str:nome>
GET /status
MENTIRA GET /perfil/<str:id>
MENTIRA GET /nome/<str:id>
MENTIRA GET /nome/bid/<str:bid>
MENTIRA GET /id/<str:nome>
MENTIRA GET /id/bid/<str:bid>
MENTIRA GET /bid/<str:nome>
MENTIRA GET /bid/id/<str:id>
MENTIRA GET /jogos/<str:bid>
MENTIRA GET /jogo/<str:mid>
"""
    }

@app.get("/usuarios")
async def usuarios() -> dict:
    """GET /usuarios"""
    return {
        "status": True,
        "message": "Porra nenhuma",
    }

@app.get("/usuario/{nome}")
async def usuario(nome: str) -> dict:
    """GET /usuario"""
    return {
        "status": True,
        "message": "Porra nenhuma",
    }

@app.get("/status")
async def status() -> dict:
    """GET /status"""
    return {
        "status": True,
        "message": "Porra nenhuma",
    }
