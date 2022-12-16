from app.session import SessionData, cookie, verifier
from app.db import database, get_user
from app.sockets import manager
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter(prefix="/team", tags=["team"])

class PokemonUpdate(BaseModel):
    name: str
    index: int
    type: str = "pokemon"

class ItemUpdate(BaseModel):
    name: str
    index: int
    type: str = "item"

@router.post("/pokemon/{index}", dependencies=[Depends(cookie)])
async def update_pokemon_by_index(index: int, update: PokemonUpdate, session_data: SessionData = Depends(verifier), db: Session = Depends(database)):
    user = get_user(db, session_data.user_id)
    setattr(user.team, f"pokemon{index}", update.name)
    db.commit()
    await manager.send_json(dict(update), user.id)

@router.post("/item/{index}", dependencies=[Depends(cookie)])
async def update_item_by_index(index: int, update: ItemUpdate, session_data: SessionData = Depends(verifier), db: Session = Depends(database)):
    user = get_user(db, session_data.user_id)
    setattr(user.team, f"item{index}", update.name)
    db.commit()
    await manager.send_json(dict(update), user.id)