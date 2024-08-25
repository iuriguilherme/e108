"""/api/v1"""

import logging, sys
logger: logging.Logger = logging.getLogger(__name__)

sites: dict[str] = {
    'br': "https://origins.habbo.com.br/api/public",
    'es': "https://origins.habbo.es/api/public",
    'en': "https://origins.habbo.com/api/public",
}

try:
    import datetime
    from fastapi import (
        APIRouter,
    )
    import os
    from quart import Quart
    from sqlalchemy import (
        create_engine,
        delete,
        MetaData,
        select,
        update,
    )
    from sqlalchemy.orm import Session
    from sqlalchemy.exc import (
        IntegrityError,
        NoResultFound,
    )
    from .common import (
        dbo_insert,
        dbo_update,
        get_json,
        get_status,
        get_text,
        sites,
    )
    from ..models.bb.v1 import (
        Base,
        Badge,
        Match,
        MatchPlayer,
        MatchTeam,
        Rank,
        User,
    )
except Exception as e:
    logger.exception(e)
    sys.exit("Erro fatal, stacktrace acima")

engine: object = create_engine(os.getenv("DB_URL",
    default = "sqlite+pysqlite:///:memory:"), echo = True)
Base.metadata.create_all(engine)

um: APIRouter = APIRouter()

@um.get("/")
async def index() -> dict:
    """GET /"""
    return {
        "status": True,
        "message": """Lista de endpoints:\
https://origins.habbo.com/api/public/api-docs/"""
    }

@um.get("/status")
async def status(lang: str = 'br') -> dict:
    """GET /ping"""
    return {
        "status": True,
        "response": await get_status("/".join([sites[lang], "ping"])),
    }

@um.get("/users")
async def users(lang: str = "br") -> dict:
    """GET /users"""
    try:
        return await get_json("/".join([sites[lang],
            "origins", "users"]))
    except Exception as e:
        return {
            "status": False,
            "message": repr(e),
        }

@um.get("/user/name/{name}")
async def user_name(name: str, lang: str = "br") -> dict:
    """GET /users?name"""
    try:
        if name not in ["", " ", None, False]:
            return await get_json("/".join([sites[lang],
                f"users?name={name}"]))
        else:
            return {
                "status": False,
                "message": "Qual é o name, porra?",
            }
    except Exception as e:
        return {
            "status": False,
            "message": repr(e),
        }

@um.get("/user/id/{uid}")
async def user_id(uid: str = "", lang: str = "br") -> dict:
    """GET /users/uid"""
    try:
        if uid not in ["", " ", None, False]:
            return await get_json("/".join([sites[lang],
                "users", f"{uid}"]))
        else:
            return {
                "status": False,
                "message": "qual é o uid, porra?",
            }
    except Exception as e:
        return {
            "status": False,
            "message": repr(e),
        }

@um.get("/player/{pid}")
async def player(pid: str = "", lang: str = "br") -> dict:
    """Get user by pid"""
    try:
        if pid not in ["", " ", None, False]:
            uid: dict = await get_text("/".join([sites[lang],
                "users", "by-playerId", f"{pid}"]))
            if uid["status"]:
                return await get_json("/".join([sites[lang],
                    "users", f"{uid['message']}"]))
            else:
                return uid
        else:
            return {
                "status": False,
                "message": "qual é o pid, porra?",
            }
    except Exception as e:
        return {
            "status": False,
            "message": repr(e),
        }

@um.get("/matches/{pid}")
async def matches(
    pid: str,
    offset: int = 0,
    limit: int = 10,
    start_time: float = (datetime.datetime.now(datetime.UTC) - 
        datetime.timedelta(days = 1)).timestamp(),
    end_time: float = datetime.datetime.now(datetime.UTC).timestamp(),
    lang: str = "br",
) -> dict:
    """GET /matches/v1/uniquePlayerId/ids"""
    try:
        if pid not in ["", " ", None, False]:
            return await get_json("/".join([sites[lang],
                "matches", "v1", f"{pid}",
                "&".join([f"ids?offset={offset}", f"limit={limit}", 
                f"""start_time=\
{datetime.datetime.fromtimestamp(
start_time).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}""",
                f"""end_time=\
{datetime.datetime.fromtimestamp(
end_time).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}"""
            ])]))
        else:
            return {
                "status": False,
                "message": "qual é o pid, porra?",
            }
    except Exception as e:
        return {
            "status": False,
            "message": repr(e),
        }

@um.get("/match/{mid}")
async def match(
    mid: str,
    lang: str = "br",
) -> dict:
    """GET /matches/v1/uniqueMatchId"""
    try:
        if mid not in ["", " ", None, False]:
            return await get_json("/".join([sites[lang],
                "matches", "v1", f"{mid}"]))
        else:
            return {
                "status": False,
                "message": "qual é o pid, porra?",
            }
    except Exception as e:
        return {
            "status": False,
            "message": repr(e),
        }

@um.get("/pid2uid")
async def pid2uid(pid: str, lang: str = "br") -> dict:
    """Get uniqueHabboId from uniquePlayerId"""
    try:
        return await get_text("/".join([sites[lang],
            "users", "by-playerId", f"{pid}"]))
    except Exception as e:
        return {
            "status": False,
            "message": repr(e),
        }

@um.get("/uid2pid")
async def uid2pid(uid: str, lang: str = "br") -> dict:
    """Get uniquePlayerId from uniqueHabboId"""
    try:
        if uid not in ["", " ", None, False]:
            user: dict = await get_json("/".join([sites[lang],
                "users", f"{uid}"]))
            if user["status"]:
                return {
                    "status": True,
                    "message": user["message"]["bouncerPlayerId"],
                }
            else:
                return user
        else:
            return {
                "status": False,
                "message": "qual é o uid, porra?",
            }
    except Exception as e:
        return {
            "status": False,
            "message": repr(e),
        }

@um.get("/name2pid")
async def name2pid(name: str, lang: str = "br") -> dict:
    """Get uniquePlayerId from name"""
    try:
        if name not in ["", " ", None, False]:
            user: dict = await get_json("/".join([sites[lang],
                f"users?name={name}"]))
            if user["status"]:
                return {
                    "status": True,
                    "message": user["message"]["bouncerPlayerId"],
                }
            else:
                return user
        else:
            return {
                "status": False,
                "message": "qual é o name, porra?",
            }
    except Exception as e:
        return {
            "status": False,
            "message": repr(e),
        }

@um.get("/name2uid")
async def name2uid(pid: str, lang: str = "br") -> dict:
    """Get uniqueHabboId from name"""
    try:
        if name not in ["", " ", None, False]:
            user: dict = await get_json("/".join([sites[lang],
                f"users?name={name}"]))
            if user["status"]:
                return {
                    "status": True,
                    "message": user["message"]["uniqueId"],
                }
            else:
                return user
        else:
            return {
                "status": False,
                "message": "qual é o name, porra?",
            }
    except Exception as e:
        return {
            "status": False,
            "message": repr(e),
        }

async def extract_participants(match_id: str,
    participants: list[dict]) -> list[MatchPlayer]:
    """Transforma os jogadores em modelos"""
    return [MatchPlayer(
            matchPlayerId = f"{match_id}_{p['gamePlayerId']}",
            gamePlayerId= str(p["gamePlayerId"]),
            gameScore = int(p["gameScore"]),
            playerPlacement = int(p["playerPlacement"]),
            teamId = int(p["teamId"]),
            teamPlacement = int(p["teamPlacement"]),
            timesStunned = int(p["timesStunned"]),
            powerUpPickups = int(p["powerUpPickups"]),
            powerUpActivations = int(p["powerUpActivations"]),
            tilesCleaned = int(p["tilesCleaned"]),
            tilesColoured = int(p["tilesColoured"]),
            tilesStolen = int(p["tilesStolen"]),
            tilesLocked = int(p["tilesLocked"]),
            tilesColouredForOpponents = int(
                p["tilesColouredForOpponents"]),
        ) for p in participants]

async def extract_teams(match_id: str, teams: list[dict]) -> list[MatchTeam]:
    """Transforma os times em modelos"""
    return [MatchTeam(
        matchTeamId = f"{match_id}_{t['teamId']}",
        teamId = int(t["teamId"]),
        win = bool(t["win"]),
        teamScore = int(t["teamScore"]),
        teamPlacement = int(t["teamPlacement"]),
    ) for t in teams]

async def extract_match(data: str) -> Match:
    """Transforma partida em modelo"""
    return Match(
        matchId = str(data["metadata"]["matchId"]),
        gameCreation = int(data["info"]["gameCreation"]),
        gameDuration = int(data["info"]["gameDuration"]),
        gameEnd = int(data["info"]["gameEnd"]),
        gameMode = str(data["info"]["gameMode"]),
        mapId = int(data["info"]["mapId"]),
        ranked = bool(data["info"]["ranked"]),
        participants = await extract_participants(
            str(data["metadata"]["matchId"]),
            data["info"]["participants"]),
        teams = await extract_teams(str(data["metadata"]["matchId"]),
            data["info"]["teams"]),
    )

async def extract_user(data: str) -> User:
    """Transforma partida em modelo"""
    return User(
        bouncerPlayerId = str(data["bouncerPlayerId"]),
        uniqueId = str(data["uniqueId"]),
        name = str(data["name"]),
        figureString = str(data["figureString"]),
        lastAccessTime = int(datetime.datetime.strptime(
            data["lastAccessTime"], "%Y-%m-%dT%H:%M:%S.%f%z").timestamp()),
        memberSince = int(datetime.datetime.strptime(
            data["memberSince"], "%Y-%m-%dT%H:%M:%S.%f%z").timestamp()),
        motto = str(data["motto"]),
        profileVisible = bool(data["profileVisible"]),
        currentLevel = int(data["currentLevel"]),
        currentLevelCompletePercent = int(data["currentLevelCompletePercent"]),
        starGemCount = int(data["starGemCount"]),
        totalExperience = int(data["totalExperience"]),
        selectedBadges = [Badge(
            code = str(b["code"]),
            badgeIndex = int(b["badgeIndex"]),
            name = str(b["name"]),
            description = str(b["description"]),
            user_id = str(data["bouncerPlayerId"]),
        ) for b in data["selectedBadges"]],
    )

async def extract_user_update(data: str) -> dict:
    """Atualiza dados variáveis"""
    return dict(
        name = str(data["name"]),
        figureString = str(data["figureString"]),
        lastAccessTime = int(datetime.datetime.strptime(
            data["lastAccessTime"], "%Y-%m-%dT%H:%M:%S.%f%z").timestamp()),
        motto = str(data["motto"]),
        profileVisible = bool(data["profileVisible"]),
        currentLevel = int(data["currentLevel"]),
        currentLevelCompletePercent = int(data["currentLevelCompletePercent"]),
        starGemCount = int(data["starGemCount"]),
        totalExperience = int(data["totalExperience"]),
    )

async def update_matches(match_ids: list[str]) -> None:
    """Atualiza banco de dados com partidas"""
    try:
        for match_id in match_ids:
            try:
                with Session(engine) as session:
                    session.scalars(select(Match).where(
                        Match.matchId == match_id)).one()
            except NoResultFound:
                _match: dict = await match(match_id)
                if _match["status"]:
                    await dbo_insert(engine, [await extract_match(_match["message"])])
    except Exception as e:
        logger.exception(e)

async def update_user(nome: str, **kwargs) -> None:
    """Atualiza usuário no banco de dados"""
    try:
        user: dict = await user_name(nome)
        if user["status"]:
            logger.info(user["message"])
            try:
                _user: dict = await extract_user(user["message"])
                await dbo_insert(engine, [_user])
            except IntegrityError as e:
                logger.exception(e)
                _user: dict = await extract_user_update(user["message"])
                await dbo_insert(engine, update(User).where(
                    User.name == nome).values(**_user))
            _matches: dict = await matches(
                user["message"]["bouncerPlayerId"], **kwargs)
            if _matches["status"]:
                await update_matches(_matches["message"])
    except Exception as e:
        logger.exception(e)

async def create_user(nome: str, **kwargs) -> None:
    """Cria usuário no banco de dados"""
    try:
        user: dict = await user_name(nome)
        if user["status"]:
            logger.info(user["message"])
            try:
                _user: dict = await extract_user(user["message"])
                await dbo_insert(engine, [_user])
            except IntegrityError as e:
                logger.exception(e)
                _user: dict = await extract_user_update(user["message"])
                await dbo_insert(engine, update(User).where(
                    User.name == nome).values(**_user))
            _matches: dict = await matches(
                user["message"]["bouncerPlayerId"], **kwargs)
            if _matches["status"]:
                await update_matches(_matches["message"])
                dias_atras: int = 1
                while kwargs["start_time"] > (datetime.datetime.now(
                    datetime.UTC) - datetime.timedelta(days = 7)).timestamp():
                    while _matches["status"] and len(_matches["message"]) > 1:
                        logger.warning(f"""matches found: \
{len(_matches['message'])}, parâmetros: {kwargs}""")
                        # ~ logger.warning(f"matches: {_matches['message']}")
                        kwargs["offset"] += kwargs["limit"]
                        _matches = await matches(
                            user["message"]["bouncerPlayerId"], **kwargs)
                        if _matches["status"]:
                            await update_matches(_matches["message"])
                    kwargs["start_time"] = (datetime.datetime.now(
                        datetime.UTC) - datetime.timedelta(days = (
                        dias_atras + 1))).timestamp()
                    kwargs["end_time"] = (datetime.datetime.now(
                        datetime.UTC) - datetime.timedelta(
                        days = dias_atras)).timestamp()
                    kwargs["offset"] = kwargs["limit"]
                    dias_atras += 1
    except Exception as e:
        logger.exception(e)

@um.get("/atualizar/{nome}")
async def atualizar(
    nome: str,
    offset: int = 0,
    limit: int = 300,
    start_time: float = (datetime.datetime.now(datetime.UTC) - 
        datetime.timedelta(days = 1)).timestamp(),
    end_time: float = datetime.datetime.now(datetime.UTC).timestamp(),
    lang: str = "br",
) -> dict:
    """GET /atualizar"""
    try:
        with Session(engine) as session:
            rank_stmt: object = select(Rank).where(Rank.nome == nome)
            try:
                rank: Rank = session.scalars(rank_stmt).one()
            except NoResultFound:
                await dbo_insert(engine, [Rank(nome = nome, pontos = 0)])
            rank: Rank = session.scalars(rank_stmt).one()
            await update_user(
                nome,
                offset = offset,
                limit = limit,
                start_time = start_time,
                end_time = end_time,
                lang = lang,
            )
            user_stmt: object = select(User).where(User.name == nome)
            try:
                ## FIXME: não tem razão pra isso não funcionar
                user_id: str = session.scalars(user_stmt).one().bouncerPlayerId
            except NoResultFound as e:
                logger.exception(e)
                user_id: str = (await name2pid(nome))["message"]
            score_stmt: object = select(MatchPlayer.gameScore).select_from(
                Match).join(MatchPlayer,
                Match.matchId == MatchPlayer.match_id).where(
                MatchPlayer.gamePlayerId == user_id, Match.ranked == 1)
            scores: object = session.scalars(score_stmt)
            await dbo_insert(engine, update(Rank).where(
                Rank.nome == nome).values(pontos = sum(scores)))
            total: int = session.scalars(select(Rank.pontos).where(
                Rank.nome == nome)).one()
        return {
            "status": True,
            "message": f"Total de pontos para {nome}: {total}",
        }
    except Exception as e:
        logger.exception(e)
        return {
            "status": False,
            "message": repr(e),
        }

@um.get("/criar/{nome}")
async def criar(
    nome: str,
    offset: int = 0,
    limit: int = 300,
    start_time: float = (datetime.datetime.now(datetime.UTC) - 
        datetime.timedelta(days = 1)).timestamp(),
    end_time: float = datetime.datetime.now(datetime.UTC).timestamp(),
    lang: str = "br",
) -> dict:
    """GET /atualizar"""
    try:
        with Session(engine) as session:
            rank_stmt: object = select(Rank).where(Rank.nome == nome)
            try:
                rank: Rank = session.scalars(rank_stmt).one()
            except NoResultFound:
                await dbo_insert(engine, [Rank(nome = nome, pontos = 0)])
            rank: Rank = session.scalars(rank_stmt).one()
            await create_user(
                nome,
                offset = offset,
                limit = limit,
                start_time = start_time,
                end_time = end_time,
                lang = lang,
            )
            user_stmt: object = select(User).where(User.name == nome)
            try:
                user_id: str = session.scalars(user_stmt).one().bouncerPlayerId
            except NoResultFound as e:
                logger.exception(e)
                user_id: str = (await name2pid(nome))["message"]
            score_stmt: object = select(MatchPlayer.gameScore).select_from(
                Match).join(MatchPlayer,
                Match.matchId == MatchPlayer.match_id).where(
                MatchPlayer.gamePlayerId == user_id, Match.ranked == 1)
            scores: object = session.scalars(score_stmt)
            await dbo_insert(engine, update(Rank).where(
                Rank.nome == nome).values(pontos = sum(scores)))
            total: int = session.scalars(select(Rank.pontos).where(
                Rank.nome == nome)).one()
        return {
            "status": True,
            "message": f"Total de pontos para {nome}: {total}",
        }
    except Exception as e:
        logger.exception(e)
        return {
            "status": False,
            "message": repr(e),
        }

@um.get("/placar")
async def placar(lang: str = "br") -> dict:
    """Retorna placar"""
    try:
        with Session(engine) as session:
            ranks: object = select(Rank)
            rankings: list[tuple] = sorted([(r.nome, r.pontos) for r in \
                session.scalars(select(Rank).where(Rank.pontos > 0))],
                    key = lambda x: x[1], reverse = True)
        return rankings
    except Exception as e:
        logger.exception(e)
        return {"Morgona": 0}

@um.get("/remove/{nome}")
async def remove(nome: str, lang: str = "br") -> dict:
    """Remove do placar"""
    try:
        with Session(engine) as session:
            remove_stmt: object = delete(Rank).where(Rank.nome == nome)
            session.execute(remove_stmt)
            session.commit()
        return {
            "status": True,
            "message": f"{nome} removido do placar",
        }
    except Exception as e:
        logger.exception(e)
        return {
            "status": False,
            "message": repr(e),
        }
