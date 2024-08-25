"""Métodos comuns às versões"""

import logging
logger: logging.Logger = logging.getLogger(__name__)

try:
    # ~ import datetime
    # ~ from fastapi import (
        # ~ APIRouter,
        # ~ FastAPI,
    # ~ )
    import requests
    # ~ import os
    # ~ from quart import Quart
    from sqlalchemy import (
        # ~ create_engine,
        delete,
        # ~ MetaData,
        select,
        update,
    )
    from sqlalchemy.orm import Session
    from sqlalchemy.exc import (
        IntegrityError,
        NoResultFound,
    )
except Exception as e:
    logger.exception(e)
    sys.exit("Erro fatal, stacktrace acima")

sites: dict[str] = {
    'br': "https://origins.habbo.com.br/api/public",
    'es': "https://origins.habbo.es/api/public",
    'en': "https://origins.habbo.com/api/public",
}

async def get_status(url: str) -> int:
    """Get HTTP status code with requests"""
    try:
        logger.info(f"GET STATUS {url}")
        response: requests.Request = requests.get(url)
        return response.status_code
    except Exception as e:
        logger.exception(e)
    ## https://github.com/joho/7XX-rfc
    return 776

async def get_text(url: str) -> dict:
    """Get text data with requests"""
    try:
        logger.info(f"GET HTML {url}")
        response: requests.Request = requests.get(url)
        if response.status_code == 200:
            data: str = response.text
            if data:
                return {
                    "status": True,
                    "message": data,
                }
    except Exception as e:
        logger.exception(e)
    return {
        "status": False,
        "message": "Servidor do Origins não retornou porra nenhuma",
    }

async def get_json(url: str) -> dict:
    """Get json data with requests"""
    try:
        logger.info(f"GET JSON {url}")
        response: requests.Request = requests.get(url)
        if response.status_code == 200:
            data: str = response.json()
            if data:
                return {
                    "status": True,
                    "message": data,
                }
    except Exception as e:
        logger.exception(e)
    return {
        "status": False,
        "message": "Servidor do Origins não retornou porra nenhuma",
    }

async def dbo_select_one(engine: object, table: str, column : str,
    value: str) -> dict:
    """Testa existência de dados do banco"""
    try:
        with Session(engine) as session:
            return {
                "status": True,
                "data": session.scalars(select(table).where(
                    column == value)).one()
            }
    except NoResultFound:
        return {"status": False}
    except Exception as e:
        logger.exception(e)
        return {"status": False}

async def dbo_insert(engine: object, queries: list[str]) -> None:
    """Persiste dados no banco"""
    try:
        with Session(engine) as session:
            session.add_all(queries)
            session.commit()
    except IntegrityError as e:
        logger.exception(e)
        logger.warning("Item already existed on database")
    except Exception as e:
        logger.exception(e)

async def dbo_update(engine: object, statement: str) -> None:
    """Atualiza dados no banco"""
    try:
        with Session(engine) as session:
            session.execute(statement)
            session.commit()
    except IntegrityError as e:
        logger.exception(e)
        logger.warning("Item already existed on database")
    except Exception as e:
        logger.exception(e)
