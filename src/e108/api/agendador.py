"""apscheduler"""

import logging
logger: logging.Logger = logging.getLogger(__name__)

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.triggers.interval import IntervalTrigger
import datetime
import os
import uuid

async def get_job_id(*args) -> str:
    """Retorna um uuid5 a partir de args"""
    return str(uuid.uuid5(uuid.UUID(int = 0), '.'.join(args)))

def get_jobstore(*args , **kwargs) -> object:
    """get jobstore"""
    try:
        return SQLAlchemyJobStore(
            *args,
            tablename = os.getenv("APS_TABLE", "job_queue"),
             **kwargs,
         )
    except Exception as e:
        logger.exception(e)
        logger.warning("""Conexão com o banco de dados para o agendador não deu \
certo, usando agendador na memória do servidor. Vai encher a memória de lixo e \
eventualmente derrubar o servidor! (Mentira, não é pra tanto. Mas que tá errado, \
tá.""")
        return MemoryJobStore()

def get_scheduler(*args, **kwargs) -> object:
    """get scheduler"""
    try:
        return AsyncIOScheduler(
            jobstores = {
                'default': get_jobstore(*args, **kwargs),
            },
            executors = {
                'default': AsyncIOExecutor(),
            },
            # ~ event_loop = asyncio.get_current_loop(),
        )
    except Exception as e:
        logger.exception(e)
        logger.warning("""Agendador assíncrono não pôde ser carregado. Um \
agendador padrão vai ser usado na memória.""")
        return BackgroundScheduler()

async def agendar(
    callback: object,
    nomes: list,
    scheduler: object,
    j_args: list = [],
    j_kwargs: dict = {},
    r_kwargs: dict = {},
    repetir: bool = False,
    j_date: dict = {"minutes": 1},
    r_date: dict = {"minutes": 15},
    **kwargs,
) -> None:
    """Cria tarefa"""
    try:
        job_id: str = (await get_job_id(*nomes))
        job: object = scheduler.add_job(
            callback,
            'date',
            args = j_args,
            kwargs = j_kwargs,
            id = job_id,
            name = job_id,
            # ~ jobstore = kwargs.get("jobstore", "default"),
            # ~ executor = kwargs.get("executor", "default"),
            replace_existing = True,
            run_date = (datetime.datetime.now() + \
                datetime.timedelta(**j_date)),
        )
        if repetir:
            try:
                scheduler.reschedule_job(
                    job_id,
                    'interval',
                    # ~ jobstore = kwargs.get("jobstore", "default"),
                    **r_kwargs,
                )
            except Exception as e:
                logger.exception(e)
                logger.warning("Tarefa não agendada!")
    except Exception as e:
        logger.exception(e)
        logger.warning("Tarefa não criada!")
