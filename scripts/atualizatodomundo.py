"""Atualiza usuários"""

import logging
logging.basicConfig(level = 'INFO')
logger: logging.Logger = logging.getLogger(__name__)

import requests
import sys
import time

api: str = "https://habborigins.com.br/api/v2"

delay: int = int(1e1)
dias: int = 21
try:
    dias = sys.argv[1]
except:
    pass

try:
    with open('docs/users.txt', 'r') as f:
        users: list[str] = [l.rstrip() for l in f]
    for user in users:
        logger.info(f"Atualizando {user}")
        time.sleep(delay)
        requests.get("/".join([api, "atualizar",
            "partidas", f"{user}?last_day={dias}&bypass=1"]))
    time.sleep(delay)
    requests.get("/".join([api, "atualizar",
        "usuarios"]))
    requests.get("/".join([api, "atualizar",
        "partidas"]))
    for user in users:
        logger.info(f"Atualizando placar para {user}")
        time.sleep(delay)
        requests.get("/".join([api, "atualizar",
            "placar", "um", f"{user}?bypass=1"]))
except Exception as e:
    logger.exception(e)
