"""Faz tantos anos que eu não vou na escola que eu não lembro o que é um dbo"""

import logging
logger: logging.Logger = logging.getLogger(__name__)

try:
    import os
    from quart import Quart
    from sqlalchemy import (
        create_engine,
        MetaData,
        select,
    )
    from sqlalchemy.orm import Session
    from .models.bb import (
        Base,
        Match,
        MatchPlayer,
        MatchTeam,
        Rank,
    )
    from .api import (
        match,
        user_name,
    )
except Exception as e:
    logger.exception(e)
    raise

async def dbo_update(queries: list[str]) -> None:
    """Persiste dados no banco"""
    try:
        engine: object = create_engine(os.getenv("DB_URL",
            default = "sqlite+pysqlite:///:memory:"), echo = True)
        Base.metadata.create_all(engine)
        with Session(engine) as session:
            session.add_all(queries)
            session.commit()
    except Exception as e:
        logger.exception(e)

async def extract_participants(participants: list[dict]) -> list[MatchPlayer]:
    """Transforma os jogadores em modelos"""
    return [MatchPlayer(
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

async def extract_teams(teams: list[dict]) -> list[MatchTeam]:
    """Transforma os times em modelos"""
    return [MatchTeam(
        teamId = int(t["teamId"]),
        win = bool(t["win"]),
        teamScore = int(t["teamScore"]),
        teamPlacement = int(t["teamPlacement"]),
    ) for t in teams]

async def extract_match(match: str) -> Match:
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
            data["info"]["participants"]),
        teams = await extract_teams(data["info"]["teams"]),
    )

async def extract_user(data: str) -> Match:
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

async def update_matches(match_ids: list[str]) -> None:
    """Atualiza banco de dados com partidas"""
    ## TODO: fazer do jeito certo quando tiver tempo que essa porra vai
    ## dar merda
    try:
        await dbo_update([await extract_match(m["message"]) for m in [
            await match(match_id) for match_id in match_ids] if m["status"]])
    except Exception as e:
        logger.exception(e)

async def update_user(nome: str) -> None:
    """Atualiza usuário no banco de dados"""
    try:
        user: dict = await user_name(nome)
        if user["status"]:
            await dbo_update(await extract_user(user["message"]))
            matches: dict = await matches(user["message"]["bouncerPlayerId"])
            if matches["status"]:
                await update_matches(matches["message"])
    except Exception as e:
        logger.exception(e)

async def update_rank(nome: str) -> None:
    """Atualiza rank de usuário"""
    try:
        session = Session(engine)
        rank: object = select(Rank).where(Rank.nome.in_([nome]))
        if not session.scalars(rank).one():
            await dbo_update(Rank(name = nome, pontos = 0))
        await update_user(nome)
        user: object = select(User).where(User.name.in_([nome]))
        user_id: str = session.scalars(rank).one().uniqueId
        score: object = (
            select(MatchPlayer)
            .join(MatchPlayer.gameScore)
            .where(MatchPlayer.gamePlayerId == user_id)
        )
        pontos: int = sum([s.gameScore for s in session.scalars(score)])
        update_rank: object = session.scalars(rank).one()
        update_rank.pontos.update(pontos)
    except Exception as e:
        logger.exception(e)

async def get_ranks(nome: str) -> list[dict]:
    """Retorna placar"""
    try:
        ranks: object = select(Rank)
        return {r.nome: r.pontos for r in session.scalars(rank)}
    except Exsception as e:
        return {"Morgona": 0}
