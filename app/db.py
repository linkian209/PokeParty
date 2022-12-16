from enum import Enum
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, create_engine
from sqlalchemy import Enum as SAEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from app.settings import Settings
import uuid

settings = Settings()
engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()

class User(base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False)
    team = relationship("Team", back_populates="user", uselist=False)
    overlay = relationship("Overlay", back_populates="user", uselist=False)


class Team(base):
    __tablename__ = "team"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="team")
    pokemon1 = Column(String(64), nullable=True)
    pokemon2 = Column(String(64), nullable=True)
    pokemon3 = Column(String(64), nullable=True)
    pokemon4 = Column(String(64), nullable=True)
    pokemon5 = Column(String(64), nullable=True)
    pokemon6 = Column(String(64), nullable=True)
    item1 = Column(String(64), nullable=True)
    item2 = Column(String(64), nullable=True)
    item3 = Column(String(64), nullable=True)
    item4 = Column(String(64), nullable=True)
    item5 = Column(String(64), nullable=True)
    item6 = Column(String(64), nullable=True)

    def as_dict(self) -> dict:
        return {
            "pokemon1": self.pokemon1,
            "pokemon2": self.pokemon2,
            "pokemon3": self.pokemon3,
            "pokemon4": self.pokemon4,
            "pokemon5": self.pokemon5,
            "pokemon6": self.pokemon6,
            "item1": self.item1,
            "item2": self.item2,
            "item3": self.item3,
            "item4": self.item4,
            "item5": self.item5,
            "item6": self.item6,
        }


class OverlayConfigs(str, Enum):
    One_by_Six = "1x6"
    Two_by_Three = "2x3"
    Three_by_Two = "3x2"
    Six_by_One = "6x1"

    @property
    def display_name(self):
        rows, cols = self.name.split("_by_")
        return f"{rows} by {cols}"


class Overlay(base):
    __tablename__ = "overlay"
    id = Column(String(32), primary_key=True)
    width = Column(Integer)
    height = Column(Integer)
    arrangement = Column(SAEnum(OverlayConfigs))
    outline_items = Column(Boolean)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="overlay")


def database():
    db = db_session()
    try:
        yield db
    finally:
        db.close()

def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user_id: int, username: str) -> User:
    db_user = User(id=user_id, username=username)
    db_user.team = create_team(db, db_user.id)
    db_user.overlay = create_overlay(db, db_user.id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_team_by_id(db: Session, team_id: int) -> Team | None:
    return db.query(Team).filter(Team.id == team_id).first()

def create_team(db: Session, user_id: int) -> Team:
    db_team = Team(user_id=user_id)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def get_overlay(db: Session, overlay_id: str) -> Overlay | None:
    return db.query(Overlay).filter(Overlay.id == overlay_id).first()

def create_overlay(db: Session, user_id: int, overlay_id: str = uuid.uuid4().hex, height: int = 600, width: int = 800, arrangement: OverlayConfigs = OverlayConfigs.One_by_Six, outline_items: bool = False) -> Overlay:
    db_overlay = Overlay(id=overlay_id, width=width, height=height, arrangement=arrangement, user_id=user_id, outline_items=outline_items)
    db.add(db_overlay)
    db.commit()
    db.refresh(db_overlay)
    return db_overlay