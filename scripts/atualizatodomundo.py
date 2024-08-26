"""Atualiza usuários"""

import logging
logging.basicConfig(level = 'INFO')
logger: logging.Logger = logging.getLogger(__name__)


import requests

api: str = "https://habborigins.com.br/api/v2"

try:
    with open('docs/users.txt', 'r') as f:
        users: list[str] = [l.rstrip() for l in f]
    for user in users:
        logger.info(f"Atualizando {user}")
        requests.get("/".join([api, "atualizar",
            "partidas", user]))
        requests.get("/".join([api, "atualizar",
            "placar", "um", user]))
except Exception as e:
    logger.exception(e)
