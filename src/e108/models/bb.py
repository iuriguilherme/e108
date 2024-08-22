"""Modelos para Battle Ball"""

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
except Exception as e:
    logger.exception(e)
    raise

try:
    class Base(DeclarativeBase):
        """Base"""
        pass

    class Rank(Base):
        """Rank"""
        __tablename__: str = "rank"
        nome: Mapped[str] = mapped_column(primary_key = True)
        pontos: Mapped[int] = mapped_column(default = 0)
    
    class User(Base):
        """User a.k.a. Habbo"""
        __tablename__: str = "user"
        
        bouncerPlayerId: Mapped[str] = mapped_column(primary_key = True)
        
        uniqueId: Mapped[str] = mapped_column()
        name: Mapped[str] = mapped_column()
        figureString: Mapped[str] = mapped_column(default = "")
        lastAccessTime: Mapped[int] = mapped_column(
            default = int(datetime.datetime.now(datetime.UTC).timestamp()))
        memberSince: Mapped[int] = mapped_column(
            default = int(datetime.datetime.fromtimestamp(
            int(1e6)).timestamp()))
        motto: Mapped[str] = mapped_column(default = "")
        profileVisible: Mapped[bool] = mapped_column(default = False)
        currentLevel: Mapped[int] = mapped_column(default = 0)
        currentLevelCompletePercent: Mapped[int] = mapped_column(default = 0)
        starGemCount: Mapped[int] = mapped_column(default = 0)
        totalExperience: Mapped[int] = mapped_column(default = 0)
        
        selectedBadges: Mapped[list["Badge"]] = relationship(
            back_populates = "user")
        # ~ matches: Mapped[list["MatchPlayer"]] = relationship(
            # ~ back_populates = "player")
    
    class Badge(Base):
        """User badge a.k.a. emblema"""
        __tablename__: str = "badge"
        
        code: Mapped[str] = mapped_column(primary_key = True)
        
        badgeIndex: Mapped[int] = mapped_column(default = 0)
        name: Mapped[str] = mapped_column(default = "")
        description: Mapped[str] = mapped_column(default = "")
        
        user_id: Mapped[str] = mapped_column(ForeignKey(
            "user.bouncerPlayerId"))
        user: Mapped["User"] = relationship(back_populates = "selectedBadges")
    
    class MatchTeam(Base):
        """Match team info"""
        __tablename__: str = "match_team"
        
        matchTeamId: Mapped[str] = mapped_column(primary_key = True)
            
        teamId: Mapped[int] = mapped_column(default = 0)
        win: Mapped[bool] = mapped_column(default = False)
        teamScore: Mapped[int] = mapped_column(default = 0)
        teamPlacement: Mapped[int] = mapped_column(default = 0)
        
        match_id: Mapped[str] = mapped_column(ForeignKey("match.matchId"))
        match: Mapped["Match"] = relationship(back_populates = "teams")
    
    class MatchPlayer(Base):
        """Match player info"""
        __tablename__: str = "match_player"
        
        matchPlayerId: Mapped[str] = mapped_column(primary_key = True)
        
        gameScore: Mapped[int] = mapped_column(default = 0)
        playerPlacement: Mapped[int] = mapped_column(default = 0)
        teamId: Mapped[int] = mapped_column(default = 0)
        teamPlacement: Mapped[int] = mapped_column(default = 0)
        timesStunned: Mapped[int] = mapped_column(default = 0)
        powerUpPickups: Mapped[int] = mapped_column(default = 0)
        powerUpActivations: Mapped[int] = mapped_column(default = 0)
        tilesCleaned: Mapped[int] = mapped_column(default = 0)
        tilesColoured: Mapped[int] = mapped_column(default = 0)
        tilesStolen: Mapped[int] = mapped_column(default = 0)
        tilesLocked: Mapped[int] = mapped_column(default = 0)
        tilesColouredForOpponents: Mapped[int] = mapped_column(default = 0)
        
        gamePlayerId: Mapped[str] = mapped_column()
        # ~ gamePlayerId: Mapped[str] = mapped_column(ForeignKey(
            # ~ "user.bouncerPlayerId"))
        # ~ player: Mapped["User"] = relationship(back_populates = "matches")
        match_id: Mapped[str] = mapped_column(ForeignKey("match.matchId"))
        match: Mapped["Match"] = relationship(back_populates = "participants")
    
    class Match(Base):
        """Battle Ball Match"""
        __tablename__: str = "match"
        matchId: Mapped[str] = mapped_column(primary_key = True)
        gameCreation: Mapped[int] = mapped_column(default = 1)
        gameDuration: Mapped[int] = mapped_column(default = 0)
        gameEnd: Mapped[int] = mapped_column(default = 1)
        gameMode: Mapped[str] = mapped_column(default = "")
        mapId: Mapped[int] = mapped_column(default = 0)
        ranked: Mapped[bool] = mapped_column(default = False)
        participants: Mapped[list["MatchPlayer"]] = relationship(
            back_populates = "match")
        teams: Mapped[list["MatchTeam"]] = relationship(
            back_populates = "match")
    
except Exception as e:
    logger.exception(e)
    raise
