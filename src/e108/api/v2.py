"""/api/v2"""

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
    # ~ import json
    import os
    from pathlib import Path
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
        MultipleResultsFound,
        NoResultFound,
    )
    import uuid
    from .common import (
        dbo_insert,
        dbo_select_one,
        dbo_update,
        get_json,
        get_status,
        get_text,
        sites,
    )
    from .v1 import (
        status,
        index,
        users,
        user_name,
        user_id,
        player,
        matches,
        match,
        pid2uid,
        uid2pid,
        name2pid,
        name2uid,
    )
    from ..models.bb.v2 import (
        Base,
        Badge,
        Leaderboard,
        LeaderboardItem,
        # ~ LeaderboardScore,
        Match,
        MatchPlayer,
        MatchTeam,
        User,
        UserAccessTime,
        UserBadge,
        UserExperience,
        UserFigureString,
        UserLevel,
        UserLevelPercent,
        UserMotto,
        UserName,
        UserStarGem,
        UserVisibility,
    )
    from .agendador import (
        get_scheduler,
        agendar,
    )
except Exception as e:
    logger.exception(e)
    sys.exit("Erro fatal, stacktrace acima")

try:
    engine: object = create_engine(os.getenv("DB_URL_2",
        default = "sqlite+pysqlite:///:memory:"), echo = True)
    Base.metadata.create_all(engine)
    agendador: object = get_scheduler(engine = engine)
    agendador.start()
except Exception as e:
    logger.exception(e)
    sys.exit("Erro fatal, stacktrace acima")

try:
    Path("instance").mkdir(parents = True, exist_ok = True)
except Exception as e:
    logger.exception(e)
    logger.warning("instance não foi criada, verifique permissões de diretório")

dois: APIRouter = APIRouter()

dois.add_api_route("/", index, methods=["GET"])
dois.add_api_route("/status", status, methods=["GET"])
dois.add_api_route("/users", users, methods=["GET"])
dois.add_api_route("/user/name/{name}", user_name, methods=["GET"])
dois.add_api_route("/user/id/{uid}", user_id, methods=["GET"])
dois.add_api_route("/player/{pid}", player, methods=["GET"])
dois.add_api_route("/matches/{pid}", matches, methods=["GET"])
dois.add_api_route("/match/{mid}", match, methods=["GET"])
dois.add_api_route("/pid2uid", pid2uid, methods=["GET"])
dois.add_api_route("/uid2pid", uid2pid, methods=["GET"])
dois.add_api_route("/name2pid", name2pid, methods=["GET"])
dois.add_api_route("/name2uid", name2uid, methods=["GET"])

async def update_user_model(user: User, new_user: dict) -> User:
    """Aumenta listas do usuário"""
    try:
        user.figure_strings.append(UserFigureString(
            uuid = str(uuid.uuid4()),
            user_id = new_user["bouncerPlayerId"],
            figureString = new_user["figureString"]))
        user.access_times.append(UserAccessTime(
            uuid = str(uuid.uuid4()),
            user_id = new_user["bouncerPlayerId"],
            lastAccessTime = int(datetime.datetime.strptime(
            new_user["lastAccessTime"],
            "%Y-%m-%dT%H:%M:%S.%f%z").timestamp())))
        user.mottos.append(UserMotto(
            uuid = str(uuid.uuid4()),
            user_id = new_user["bouncerPlayerId"],
            motto = new_user["motto"]))
        user.profile_visibilities.append(UserVisibility(
            uuid = str(uuid.uuid4()),
            user_id = new_user["bouncerPlayerId"],
            profileVisible = new_user["profileVisible"]))
        user.levels.append(UserLevel(
            uuid = str(uuid.uuid4()),
            user_id = new_user["bouncerPlayerId"],
            currentLevel = new_user["currentLevel"]))
        user.level_percents.append(UserLevelPercent(
            uuid = str(uuid.uuid4()),
            user_id = new_user["bouncerPlayerId"],
            currentLevelCompletePercent = \
            new_user["currentLevelCompletePercent"]))
        user.star_gems.append(UserStarGem(
            uuid = str(uuid.uuid4()),
            user_id = new_user["bouncerPlayerId"],
            starGemCount = new_user["starGemCount"]))
        user.experiences.append(UserExperience(
            uuid = str(uuid.uuid4()),
            user_id = new_user["bouncerPlayerId"],
            totalExperience = new_user["totalExperience"]))
    except Exception as e:
            logger.exception(e)
    return user

async def extract_user(user: dict, lang: str = "br") -> User:
    """Transforma usuário em modelo"""
    try:
        u: User = User(
            uniqueId = str(user["uniqueId"]),
            bouncerPlayerId = str(user["bouncerPlayerId"]),
            name = str(user["name"]),
            figureString = str(user["figureString"]),
            lastAccessTime = int(datetime.datetime.strptime(
                user.get("lastAccessTime", "1970-01-01T00:00:00.000+0000"),
                "%Y-%m-%dT%H:%M:%S.%f%z").timestamp()),
            memberSince = int(datetime.datetime.strptime(
                user["memberSince"], "%Y-%m-%dT%H:%M:%S.%f%z").timestamp()),
            motto = str(user["motto"]),
            profileVisible = bool(user["profileVisible"]),
            currentLevel = int(user.get("currentLevel", 0)),
            currentLevelCompletePercent = int(user.get(
                "currentLevelCompletePercent", 0)),
            starGemCount = int(user.get("starGemCount", 0)),
            totalExperience = int(user.get("totalExperience", 0)),
        )
        u = await update_user_model(u, user)
        for badge in user.get("selectedBadges", []):
            try:
                try:
                    with Session(engine) as session:
                        session.scalars(select(Badge).where(
                            Badge.code == badge["code"])).one()
                except NoResultFound:
                    logger.warning(f"""Badge {badge['code']} was not in \
database, adding now""")
                    await dbo_insert(engine, [Badge(
                        code = str(badge["code"]),
                        name = str(badge["name"]),
                        description = str(badge["description"]),
                    )])
                u.selectedBadges.append(UserBadge(
                    uuid = str(uuid.uuid4()),
                    badge_id = str(badge["code"]),
                    user_id = str(user["bouncerPlayerId"]),
                    badgeIndex = int(badge["badgeIndex"]),
                ))
            except Exception as e:
                logger.exception(e)
        return u
    except Exception as e:
        logger.exception(e)
        return None

async def update_user(*args, **kwargs) -> None:
    """Atualiza ou cria dados do usuário no banco de dados"""
    try:
        new_user: object = await user_name(kwargs["nome"])
        if new_user["status"]:
            user_object: dict = new_user["message"]
            try:
                with Session(engine) as session:
                    user_model: object = session.scalars(select(User).where(
                        User.bouncerPlayerId == user_object["bouncerPlayerId"]
                        )).one()
                    # ~ try:
                        # ~ session.scalars(select(UserFigureString).where(
                            # ~ UserFigureString.figureString == \
                            # ~ new_user["figureString"]
                        # ~ )).one()
                    # ~ except NoResultFound:
                        # ~ pass
                    # ~ user.figure_strings.append(UserFigureString(
                        # ~ user_id = user["bouncerPlayerId"],
                        # ~ figureString = new_user["figureString"]))
                    # ~ user.access_times.append(UserAccessTime(
                        # ~ user_id = new_user["bouncerPlayerId"],
                        # ~ lastAccessTime = new_user["lastAccessTime"]))
                    # ~ user.mottos.append(UserMotto(
                        # ~ user_id = new_user["bouncerPlayerId"],
                        # ~ motto = new_user["motto"]))
                    # ~ user.profile_visibilities.append(UserVisibility(
                        # ~ user_id = new_user["bouncerPlayerId"],
                        # ~ profileVisible = new_user["profileVisible"]))
                    # ~ user.levels.append(UserLevel(
                        # ~ user_id = new_user["bouncerPlayerId"],
                        # ~ currentLevel = new_user["currentLevel"]))
                    # ~ user.level_percents.append(UserLevelPercent(
                        # ~ user_id = new_user["bouncerPlayerId"],
                        # ~ currentLevelCompletePercent = \
                        # ~ new_user["currentLevelCompletePercent"]))
                    # ~ user.star_gems.append(UserStarGem(
                        # ~ user_id = new_user["bouncerPlayerId"],
                        # ~ starGemCount = new_user["starGemCount"]))
                    # ~ user.experiences.append(UserExperience(
                        # ~ user_id = new_user["bouncerPlayerId"],
                        # ~ totalExperience = new_user["totalExperience"]))
                    # ~ user.updateTime = int(datetime.datetime.now(
                        # ~ datetime.UTC).timestamp())
                    # ~ session.commit()
                logger.info(f"""Usuário {kwargs["nome"]} dados atualizados \
(mentira)""")
            except NoResultFound:
                insert_user: object | None = \
                    await extract_user(new_user["message"])
                if insert_user:
                    await dbo_insert(engine, [insert_user])
                    logger.info(f"""Usuário {kwargs["nome"]} adicionado ao \
banco de dados""")
                else:
                    logger.warning(f"""Usuário {kwargs["nome"]} NÃO adicionado ao \
banco de dados""")
        else:
            logger.warning(f"""Usuário {kwargs["nome"]} não encontrado na API do \
Origins""")
    except Exception as e:
        logger.exception(e)

@dois.get("/atualizar/usuario/{nome}")
async def atualizar_usuario(
    nome: str,
    delay: int = 1,
    repetir: int = 0,
    r_days: int = 0,
    r_hours: int = 0,
    r_minutes: int = 0,
    lang: str = "br",
    jobstore: str = "default",
) -> dict:
    """Atualiza usuário no banco de dados"""
    try:
        r_kwargs: dict = {}
        if r_days > 0:
            r_kwargs["days"] = r_days
        elif r_hours > 0:
            r_kwargs["hours"] = r_hours
        elif r_minutes > 0:
            r_kwargs["minutes"] = r_minutes
        await agendar(
            update_user,
            ["usuario", nome],
            agendador,
            j_kwargs = {"nome": nome, "lang": lang},
            j_date = {"minutes": delay},
            repetir = bool(repetir),
            r_kwargs = r_kwargs,
            jobstore = jobstore,
        )
        return {
            "status": True,
            "message": f"""Usuária(o) {nome} agendada(o) para ser adicionada(o) \
ao banco de dados""",
        }
    except Exception as e:
        logger.exception(e)
        return {
            "status": False,
            "message": repr(e),
        }
    return {
        "status": False,
        "message": "Não deu certo",
    }

async def extract_participant(match_id: str, participant: dict,
    lang: str = "br") -> MatchPlayer:
    """Transforma jogador em modelo"""
    try:
        try:
            with Session(engine) as session:
                session.scalars(select(User).where(
                    User.bouncerPlayerId == \
                    participant["gamePlayerId"])).one()
        except NoResultFound:
            player_id: dict = await pid2uid(participant["gamePlayerId"])
            if player_id["status"]:
                new_player: dict = await user_id(player_id["message"])
                if new_player["status"]:
                    await update_user({"name": new_player["message"]["name"],
                        "lang": lang})
                else:
                    logger.warning(f"""Usuário {player_id['message']} \
não encontrado""")
            else:
                logger.warning(f"""Usuário {participant['gamePlayerId']} \
não encontrado""")
    except Exception as e:
        logger.exception(e)
    return MatchPlayer(
        uuid = str(uuid.uuid4()),
        match_id = match_id,
        user_id = f"{participant['gamePlayerId']}",
        teamId = int(participant["teamId"]),
        gameScore = int(participant["gameScore"]),
        playerPlacement = int(participant["playerPlacement"]),
        teamPlacement = int(participant["teamPlacement"]),
        timesStunned = int(participant["timesStunned"]),
        powerUpPickups = int(participant["powerUpPickups"]),
        powerUpActivations = int(participant["powerUpActivations"]),
        tilesCleaned = int(participant["tilesCleaned"]),
        tilesColoured = int(participant["tilesColoured"]),
        tilesStolen = int(participant["tilesStolen"]),
        tilesLocked = int(participant["tilesLocked"]),
        tilesColouredForOpponents = int(
            participant["tilesColouredForOpponents"]),
    )

async def extract_team(match_id: str, team: dict,
    lang: str = "br") -> MatchTeam:
    """Transforma time em modelo"""
    return MatchTeam(
        uuid = str(uuid.uuid4()),
        teamId = int(team["teamId"]),
        match_id = f"{match_id}",
        win = bool(team["win"]),
        teamScore = int(team["teamScore"]),
        teamPlacement = int(team["teamPlacement"]),
    )

async def extract_match(new_match: dict, lang: str = "br") -> Match:
    """Transforma partida em modelo"""
    return Match(
        matchId = str(new_match["metadata"]["matchId"]),
        gameCreation = int(new_match["info"]["gameCreation"]),
        gameDuration = int(new_match["info"]["gameDuration"]),
        gameEnd = int(new_match["info"]["gameEnd"]),
        gameMode = str(new_match["info"]["gameMode"]),
        mapId = int(new_match["info"]["mapId"]),
        ranked = bool(new_match["info"]["ranked"]),
        teams = [await extract_team(str(new_match["metadata"]["matchId"]),
            team) for team in new_match["info"]["teams"]],
        participants = [await extract_participant(
            new_match["metadata"]["matchId"], participant) \
            for participant in new_match["info"]["participants"]],
    )

async def update_matches(match_ids: list[str], lang: str = "br") -> None:
    """Atualiza banco de dados com partidas"""
    try:
        new_matches: list = []
        for match_id in match_ids:
            new_match: dict = await match(match_id)
            if new_match["status"]:
                try:
                    with Session(engine) as session:
                        session.scalars(select(Match).where(
                            Match.matchId == match_id)).one()
                        for participant in \
                            new_match["message"]["info"]["participants"]:
                            try:
                                with Session(engine) as session:
                                    session.scalars(select(MatchPlayer).where(
                                        MatchPlayer.user_id == \
                                        participant["gamePlayerId"]).where(
                                        MatchPlayer.match_id == \
                                        new_match["message"]["metadata"
                                        ]["matchId"])).one()
                            except NoResultFound:
                                new_matches.append(await extract_participant(
                                    match_id, participant))
                except NoResultFound:
                    new_matches.append(await extract_match(
                        new_match["message"]))
            else:
                logger.warning(f"Partida {match_id} não encontrada")
        await dbo_insert(engine, new_matches)
    except Exception as e:
        logger.exception(e)

async def update_user_matches(*args, **kwargs) -> None:
    """Atualiza banco de dados com partidas de usuário"""
    try:
        await update_user(**kwargs)
        new_matches: dict = dict()
        all_matches: set = set()
        days_ago: int = 1
        agora: datetime.datetime = datetime.datetime.now(datetime.UTC)
        new_user: object = await name2pid(kwargs["nome"])
        if new_user["status"]:
            user_id: dict = new_user["message"]
            last_start: float = (agora - \
                datetime.timedelta(days = kwargs["last_day"])).timestamp()
            last_end: float = (agora - \
                datetime.timedelta(days = (kwargs["last_day"] - 1))
                    ).timestamp()
            while (last_start <= kwargs["start_time"]) and \
                (last_end <= kwargs["end_time"]):
                while kwargs["offset"] <= kwargs["last_offset"]:
                    new_matches = await matches(user_id, **kwargs)
                    logger.info(f"""matches found: \
{len(new_matches['message'])}, all matches: {len(all_matches)}, args: \
{kwargs}""")
                    if new_matches["status"]:
                        all_matches.update(new_matches["message"])
                    kwargs["offset"] += kwargs["limit"]
                kwargs["offset"] = 0
                kwargs["start_time"] = (agora - \
                    datetime.timedelta(days = (days_ago + 1))).timestamp()
                kwargs["end_time"] = (agora - datetime.timedelta(
                    days = days_ago)).timestamp()
                days_ago += 1
            await update_matches(all_matches)
            logger.info(f"""Partidas da(o) usuária(o) {kwargs["nome"]} \
adicionadas ao banco de dados""")
        else:
            logger.warning(f"""Usuário {kwargs["nome"]} não encontrado na API do \
Origins""")
    except Exception as e:
        logger.exception(e)

@dois.get("/atualizar/partidas/{nome}")
async def atualizar_partidas(
    nome: str,
    offset: int = 0,
    limit: int = 100,
    start_time: float = (datetime.datetime.now(datetime.UTC) - \
        datetime.timedelta(days = 1)).timestamp(),
    end_time: float = (datetime.datetime.now(datetime.UTC)).timestamp(),
    last_offset: int = 3000,
    last_day: int = 21,
    delay: int = 1,
    repetir: int = 0,
    r_days: int = 0,
    r_hours: int = 0,
    r_minutes: int = 0,
    lang: str = "br",
    jobstore: str = "default",
) -> dict:
    """Atualiza partidas no banco de dados"""   
    try:
        r_kwargs: dict = {}
        if r_days > 0:
            r_kwargs["days"] = r_days
        elif r_hours > 0:
            r_kwargs["hours"] = r_hours
        elif r_minutes > 0:
            r_kwargs["minutes"] = r_minutes
        await agendar(
            update_user_matches,
            ["partidas", nome],
            agendador,
            j_kwargs = {
                "nome": nome,
                "offset": offset,
                "limit": limit,
                "start_time": start_time,
                "end_time": end_time,
                "last_offset": last_offset,
                "last_day": last_day,
                "lang": lang,
            },
            j_date = {"minutes": delay},
            repetir = bool(repetir),
            r_kwargs = r_kwargs,
            jobstore = jobstore,
        )
        return {
            "status": True,
            "message": f"""Partidas da(o) usuária(o) {nome} \
agendadas para serem adicionadas ao banco de dados""",
        }
    except Exception as e:
        logger.exception(e)
        return {
            "status": False,
            "message": repr(e),
        }
    return {
        "status": False,
        "message": "Não deu certo",
    }

async def update_leaderboard_user(*args, **kwargs) -> None:
    """Atualiza placar de usuário com total de pontuação"""
    try:
        await update_user(**kwargs)
        with Session(engine) as session:
            placar_stmt: object = select(Leaderboard).where(
                Leaderboard.description == kwargs["placar"])
            try:
                placar_object: Leaderboard = session.scalars(placar_stmt).one()
            except NoResultFound:
                placar_object: Leaderboard = Leaderboard(
                    uuid = str(uuid.uuid4()), description = kwargs["placar"])
                session.add(placar_object)
            user_stmt: object = select(User).where(User.name == kwargs["nome"])
            try:
                ## FIXME: não tem razão pra isso não funcionar
                user_id: str = session.scalars(user_stmt).one().bouncerPlayerId
            except NoResultFound:
                user_id: str = (await name2pid(kwargs["nome"]))["message"]
            scores_stmt: object = select(Match).where(Match.ranked == True)
            scores: object = session.scalars(scores_stmt).all()
            mps: list = []
            for s in scores:
                for p in s.participants:
                    if p.user_id == user_id:
                        mps.append(p.gameScore)
            total: int = sum([s.gameScore for p in scores for s in \
                p.participants if s.user_id == user_id])
            score_stmt: object = select(LeaderboardItem).where(
                LeaderboardItem.leaderboard_id == placar_object.uuid,
                LeaderboardItem.name == kwargs["nome"])
            try:
                score_object: LeaderboardItem = session.scalars(
                    score_stmt).one()
            except NoResultFound:
                score_object: LeaderboardItem = LeaderboardItem(
                    uuid = str(uuid.uuid4()),
                    name = kwargs["nome"],
                    leaderboard_id = placar_object.uuid,
                    # ~ user_id = user_id,
                )
                session.add(score_object)
            # ~ score_object.scores.append(LeaderboardScore(
                # ~ leaderboard_item_id = score_object.uuid,
                # ~ score = total
            # ~ ))
            score_object.score = total
            score_object.updateTime = int(datetime.datetime.now(
                datetime.UTC).timestamp())
            # ~ try:
                # ~ session.scalars(select(LeaderboardItem).where(
                # ~ LeaderboardItem.leaderboard_id == placar_object.uuid,
                # ~ LeaderboardItem.user_id == user_id)).first()
            # ~ except NoResultFound:
                # ~ placar_object.items.append(score_object)
            # ~ except MultipleResultsFound:
                # ~ pass
            session.commit()
        logger.info(f"Total de pontos para {kwargs['nome']}: {total}")
    except Exception as e:
        logger.exception(e)

@dois.get("/atualizar/placar/{placar}/{nome}")
async def atualizar_placar_usuario(
    placar: str,
    nome: str,
    delay: int = 1,
    repetir: int = 0,
    r_days: int = 0,
    r_hours: int = 0,
    r_minutes: int = 0,
    lang: str = "br",
    jobstore: str = "default",
) -> dict:
    """Atualiza partidas no banco de dados"""   
    try:
        r_kwargs: dict = {}
        if r_days > 0:
            r_kwargs["days"] = r_days
        elif r_hours > 0:
            r_kwargs["hours"] = r_hours
        elif r_minutes > 0:
            r_kwargs["minutes"] = r_minutes
        await agendar(
            update_leaderboard_user,
            ["placar", placar, nome],
            agendador,
            j_kwargs = {
                "nome": nome,
                "placar": placar,
                "lang": lang,
            },
            j_date = {"minutes": delay},
            repetir = bool(repetir),
            r_kwargs = r_kwargs,
            jobstore = jobstore,
        )
        return {
            "status": True,
            "message": f"""Pontos de {nome} no placar {placar} \
agendados para serem adicionadas ao banco de dados""",
        }
    except Exception as e:
        logger.exception(e)
        return {
            "status": False,
            "message": repr(e),
        }
    return {
        "status": False,
        "message": "Não deu certo",
    }

@dois.get("/placar/{placar}")
async def get_placar(placar: str, lang: str = "br") -> dict:
    """Retorna placar"""
    try:
        with Session(engine) as session:
            placar_stmt: object = select(Leaderboard).where(
                Leaderboard.description == placar)
            try:
                placar_object: Leaderboard = session.scalars(placar_stmt).one()
            except NoResultFound:
                placar_object: Leaderboard = Leaderboard(
                uuid = str(uuid.uuid4()), description = placar)
                session.add(placar_object)
                session.commit()
            rankings: list[tuple] = sorted([(r.name, r.score) for r in \
                placar_object.items],
                    key = lambda x: x[1], reverse = True)
            return {
                "status": True,
                "message": rankings,
            }
        return rankings
    except Exception as e:
        logger.exception(e)
        return {
            "status": False,
            "message": repr(e),
        }
