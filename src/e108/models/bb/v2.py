"""Modelos para Battle Ball (versão 2)"""

## TODO: Usar alembic que nem eu fazia quando era um bom programador

import logging
logger: logging.Logger = logging.getLogger(__name__)

try:
    import datetime
    from sqlalchemy import (
        ForeignKey,
        String,
    )
    from sqlalchemy.orm import (
        DeclarativeBase,
        Mapped,
        mapped_column,
        relationship,
    )
    import uuid
except Exception as e:
    logger.exception(e)
    raise

try:
    class Base(DeclarativeBase):
        """Base"""
        pass

    class Leaderboard(Base):
        """Placar"""
        __tablename__: str = "leaderboard"
        uuid: Mapped[str] = mapped_column(String(36), primary_key = True,
            default = str(uuid.uuid4()))
        items: Mapped[list["LeaderboardItem"]] = relationship()
        updateTime: Mapped[int] = mapped_column(
            default = int(datetime.datetime.now(datetime.UTC).timestamp()))
        description: Mapped[str] = mapped_column(String(255),
            default = "placar")
    
    class LeaderboardItem(Base):
        """Item do placar"""
        __tablename__: str = "leaderboard_item"
        uuid: Mapped[str] = mapped_column(String(36), primary_key = True,
            default = str(uuid.uuid4()))
        leaderboard_id: Mapped[str] = mapped_column(String(36), 
            ForeignKey("leaderboard.uuid"), unique = False)
        name: Mapped[str] = mapped_column(String(255))
        # ~ user_id: Mapped[str] = mapped_column(String(36),
            # ~ ForeignKey("user.uuid"),
            # ~ unique = False)
        # ~ scores: Mapped[list["LeaderboardScore"]] = relationship()
        updateTime: Mapped[int] = mapped_column(
            default = int(datetime.datetime.now(datetime.UTC).timestamp()))
        score: Mapped[int] = mapped_column(default = 0)
    
    # ~ class LeaderboardScore(Base):
        # ~ """Pontuação"""
        # ~ __tablename__: str = "leaderboard_score"
        # ~ uuid: Mapped[str] = mapped_column(String(36), primary_key = True,
            # ~ default = str(uuid.uuid4()))
        # ~ leaderboard_item_id: Mapped[str] = mapped_column(String(36),
            # ~ ForeignKey("leaderboard_item.uuid"),
            # ~ unique = False)
        # ~ updateTime: Mapped[int] = mapped_column(
            # ~ default = int(datetime.datetime.now(datetime.UTC).timestamp()))
        # ~ score: Mapped[int] = mapped_column(default = 0)
    
    class User(Base):
        """User a.k.a. Habbo"""
        __tablename__: str = "user"
        uuid: Mapped[str] = mapped_column(String(36), primary_key = True,
            default = str(uuid.uuid4()))
        profile_visibilities: Mapped[list["UserVisibility"]] = relationship()
        levels: Mapped[list["UserLevel"]] = relationship()
        level_percents: Mapped[list["UserLevelPercent"]] = relationship()
        star_gems: Mapped[list["UserStarGem"]] = relationship()
        experiences: Mapped[list["UserExperience"]] = relationship()
        access_times: Mapped[list["UserAccessTime"]] = relationship()
        figure_strings: Mapped[list["UserFigureString"]] = relationship()
        mottos: Mapped[list["UserMotto"]] = relationship()
        names: Mapped[list["UserName"]] = relationship()
        selectedBadges: Mapped[list["UserBadge"]] = relationship()
        # ~ matches: Mapped[list["Match"]] = relationship()
        uniqueId: Mapped[str] = mapped_column(String(255), unique = True)
        bouncerPlayerId: Mapped[str] = mapped_column(String(255),
            unique = True)
        memberSince: Mapped[int] = mapped_column(
            default = int(datetime.datetime.fromtimestamp(
            int(1e6)).timestamp()))
        updateTime: Mapped[int] = mapped_column(
            default = int(datetime.datetime.now(datetime.UTC).timestamp()))
        name: Mapped[str] = mapped_column(String(255), default = "Ninguem")
        figureString: Mapped[str] = mapped_column(String(255), default = "")
        motto: Mapped[str] = mapped_column(String(255), default = "")
        profileVisible: Mapped[bool] = mapped_column(default = False)
        currentLevel: Mapped[int] = mapped_column(default = 0)
        currentLevelCompletePercent: Mapped[int] = mapped_column(default = 0)
        starGemCount: Mapped[int] = mapped_column(default = 0)
        totalExperience: Mapped[int] = mapped_column(default = 0)
        lastAccessTime: Mapped[int] = mapped_column(
            default = int(datetime.datetime.now(datetime.UTC).timestamp()))
    
    class UserMotto(Base):
        """Missão"""
        __tablename__: str = "user_motto"
        uuid: Mapped[str] = mapped_column(String(36), primary_key = True,
            default = str(uuid.uuid4()))
        user_id: Mapped[str] = mapped_column(String(36), 
            ForeignKey("user.uuid"), unique = False,
            nullable = True)
        updateTime: Mapped[int] = mapped_column(
            default = int(datetime.datetime.now(datetime.UTC).timestamp()))
        motto: Mapped[str] = mapped_column(String(255), default = "")
    
    class UserAccessTime(Base):
        """Hora de login"""
        __tablename__: str = "user_access_time"
        uuid: Mapped[str] = mapped_column(String(36), primary_key = True,
            default = str(uuid.uuid4()))
        user_id: Mapped[str] = mapped_column(String(36),
            ForeignKey("user.uuid"), unique = False,
            nullable = True)
        updateTime: Mapped[int] = mapped_column(
            default = int(datetime.datetime.now(datetime.UTC).timestamp()))
        lastAccessTime: Mapped[int] = mapped_column(
            default = int(datetime.datetime.now(datetime.UTC).timestamp()))
    
    class UserFigureString(Base):
        """Visual"""
        __tablename__: str = "user_figure_string"
        uuid: Mapped[str] = mapped_column(String(36), primary_key = True,
            default = str(uuid.uuid4()))
        user_id: Mapped[str] = mapped_column(String(36),
            ForeignKey("user.uuid"), unique = False,
            nullable = True)
        updateTime: Mapped[int] = mapped_column(
            default = int(datetime.datetime.now(datetime.UTC).timestamp()))
        figureString: Mapped[str] = mapped_column(String(255), default = "")
    
    class UserName(Base):
        """Nome"""
        __tablename__: str = "user_name"
        uuid: Mapped[str] = mapped_column(String(36), primary_key = True,
            default = str(uuid.uuid4()))
        user_id: Mapped[str] = mapped_column(String(36),
            ForeignKey("user.uuid"), unique = False,
            nullable = True)
        updateTime: Mapped[int] = mapped_column(
            default = int(datetime.datetime.now(datetime.UTC).timestamp()))
        name: Mapped[str] = mapped_column(String(255), default = "Ninguem")
    
    class UserVisibility(Base):
        """profileVisible"""
        __tablename__: str = "user_visibility"
        uuid: Mapped[str] = mapped_column(String(36), primary_key = True,
            default = str(uuid.uuid4()))
        user_id: Mapped[str] = mapped_column(String(36),
            ForeignKey("user.uuid"), unique = False,
            nullable = True)
        updateTime: Mapped[int] = mapped_column(
            default = int(datetime.datetime.now(datetime.UTC).timestamp()))
        profileVisible: Mapped[bool] = mapped_column(default = False)
    
    class UserLevel(Base):
        """currentLevel"""
        __tablename__: str = "user_level"
        uuid: Mapped[str] = mapped_column(String(36), primary_key = True,
            default = str(uuid.uuid4()))
        user_id: Mapped[str] = mapped_column(String(36),
            ForeignKey("user.uuid"), unique = False,
            nullable = True)
        updateTime: Mapped[int] = mapped_column(
            default = int(datetime.datetime.now(datetime.UTC).timestamp()))
        currentLevel: Mapped[int] = mapped_column(default = 0)
    
    class UserLevelPercent(Base):
        """currentLevelCompletePercent"""
        __tablename__: str = "user_level_percent"
        uuid: Mapped[str] = mapped_column(String(36), primary_key = True,
            default = str(uuid.uuid4()))
        user_id: Mapped[str] = mapped_column(String(36),
            ForeignKey("user.uuid"), unique = False,
            nullable = True)
        updateTime: Mapped[int] = mapped_column(
            default = int(datetime.datetime.now(datetime.UTC).timestamp()))
        currentLevelCompletePercent: Mapped[int] = mapped_column(default = 0)
    
    class UserStarGem(Base):
        """starGemCount"""
        __tablename__: str = "user_star_gem"
        uuid: Mapped[str] = mapped_column(String(36), primary_key = True,
            default = str(uuid.uuid4()))
        user_id: Mapped[str] = mapped_column(String(36),
            ForeignKey("user.uuid"), unique = False,
            nullable = True)
        updateTime: Mapped[int] = mapped_column(
            default = int(datetime.datetime.now(datetime.UTC).timestamp()))
        starGemCount: Mapped[int] = mapped_column(default = 0)
    
    class UserExperience(Base):
        """totalExperience"""
        __tablename__: str = "user_experience"
        uuid: Mapped[str] = mapped_column(String(36), primary_key = True,
            default = str(uuid.uuid4()))
        user_id: Mapped[str] = mapped_column(String(36),
            ForeignKey("user.uuid"), unique = False,
            nullable = True)
        updateTime: Mapped[int] = mapped_column(
            default = int(datetime.datetime.now(datetime.UTC).timestamp()))
        totalExperience: Mapped[int] = mapped_column(default = 0)
    
    class UserBadge(Base):
        """User badge a.k.a. emblema"""
        __tablename__: str = "user_badge"
        badge_id: Mapped[str] = mapped_column(String(255),
            ForeignKey("badge.code"),
            primary_key = True)
        user_id: Mapped[str] = mapped_column(String(36),
            ForeignKey("user.uuid"), unique = False,
            nullable = True)
        updateTime: Mapped[int] = mapped_column(
            default = int(datetime.datetime.now(datetime.UTC).timestamp()))
        badgeIndex: Mapped[int] = mapped_column(default = 0)
    
    class Badge(Base):
        """Emblema"""
        __tablename__: str = "badge"
        code: Mapped[str] = mapped_column(String(255), primary_key = True)
        updateTime: Mapped[int] = mapped_column(
            default = int(datetime.datetime.now(datetime.UTC).timestamp()))
        name: Mapped[str] = mapped_column(String(255), default = "")
        description: Mapped[str] = mapped_column(String(255), default = "")
    
    class MatchTeam(Base):
        """Match team info"""
        __tablename__: str = "match_team"
        uuid: Mapped[str] = mapped_column(String(36), primary_key = True,
            default = str(uuid.uuid4()))
        teamId: Mapped[int] = mapped_column(unique = False)
        match_id: Mapped[str] = mapped_column(String(255),
            ForeignKey("match.matchId"), unique = False,
            nullable = True)
        # ~ players: Mapped[list["MatchPlayer"]] = relationship()
        updateTime: Mapped[int] = mapped_column(
            default = int(datetime.datetime.now(datetime.UTC).timestamp()))
        win: Mapped[bool] = mapped_column(default = False)
        teamScore: Mapped[int] = mapped_column(default = 0)
        teamPlacement: Mapped[int] = mapped_column(default = 0)
    
    class MatchPlayer(Base):
        """Match player info"""
        __tablename__: str = "match_player"
        uuid: Mapped[str] = mapped_column(String(36), primary_key = True,
            default = str(uuid.uuid4()))
        match_id: Mapped[str] = mapped_column(String(36),
            ForeignKey("match.uuid"), unique = False,
            nullable = True)
        user_id: Mapped[str] = mapped_column(String(36),
            ForeignKey("user.uuid"), unique = False,
            nullable = True)
        team_id: Mapped[int] = mapped_column(ForeignKey("match_team.teamId"),
            unique = False, nullable = True)
        # ~ player: Mapped["User"] = relationship(
            # ~ back_populates = "matches")
        updateTime: Mapped[int] = mapped_column(
            default = int(datetime.datetime.now(datetime.UTC).timestamp()))
        gameScore: Mapped[int] = mapped_column(default = 0)
        playerPlacement: Mapped[int] = mapped_column(default = 0)
        teamPlacement: Mapped[int] = mapped_column(default = 0)
        timesStunned: Mapped[int] = mapped_column(default = 0)
        powerUpPickups: Mapped[int] = mapped_column(default = 0)
        powerUpActivations: Mapped[int] = mapped_column(default = 0)
        tilesCleaned: Mapped[int] = mapped_column(default = 0)
        tilesColoured: Mapped[int] = mapped_column(default = 0)
        tilesStolen: Mapped[int] = mapped_column(default = 0)
        tilesLocked: Mapped[int] = mapped_column(default = 0)
        tilesColouredForOpponents: Mapped[int] = mapped_column(default = 0)
    
    # ~ class MatchMap(Base):
        # ~ """Battle Ball Match"""
        # ~ __tablename__: str = "match_map"
        # ~ mapId: Mapped[int] = mapped_column(primary_key = True)
        # ~ updateTime: Mapped[int] = mapped_column(
            # ~ default = int(datetime.datetime.now(datetime.UTC).timestamp()))
        # ~ description: Mapped[int] = mapped_column()
    
    class Match(Base):
        """Battle Ball Match"""
        __tablename__: str = "match"
        uuid: Mapped[str] = mapped_column(String(36), primary_key = True,
            default = str(uuid.uuid4()))
        matchId: Mapped[str] = mapped_column(String(255), unique = True)
        teams: Mapped[list["MatchTeam"]] = relationship()
        participants: Mapped[list["MatchPlayer"]] = relationship()
        ## TODO: Criar modelo para mapa
        mapId: Mapped[int] = mapped_column(default = 0)
        updateTime: Mapped[int] = mapped_column(
            default = int(datetime.datetime.now(datetime.UTC).timestamp()))
        gameCreation: Mapped[int] = mapped_column(default = int(1e6))
        gameDuration: Mapped[int] = mapped_column(default = 0)
        gameEnd: Mapped[int] = mapped_column(default = int(1e6))
        gameMode: Mapped[str] = mapped_column(String(255), default = "BOUNCER")
        ranked: Mapped[bool] = mapped_column(default = False)
    
except Exception as e:
    logger.exception(e)
    raise
