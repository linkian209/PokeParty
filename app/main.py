from typing import List, Optional
from uuid import UUID
from app.db import get_user, database, OverlayConfigs
from app.settings import Settings
from app.session import cookie, backend
from app.routers import auth, team, overlay
from app.sockets import manager
from fastapi import Depends, FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from uuid import uuid4
import json


settings = Settings()
app = FastAPI(title="PokeParty")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth.router)
app.include_router(team.router)
app.include_router(overlay.router)
templates = Jinja2Templates(directory="templates")

class StaticData:
    def __init__(self):
        with open("static/data/pokemon.json","r") as f:
            raw_pokemon = json.load(f)
        with open("static/data/item-map.json", "r") as f:
            raw_items = json.load(f)
        self.pokemon = [{"slug":raw_pokemon[x]["slug"]["eng"], "name": raw_pokemon[x]["name"]["eng"]} for x in raw_pokemon]
        items = [raw_items[x].split('/')[1] if raw_items[x].split('/')[0] == "hold-item" else None for x in raw_items]
        self.items = list(filter(lambda x: x is not None, items))

    def __call__(self) -> dict:
        return {"items": self.items, "pokemon": self.pokemon}


static_data = StaticData()

@app.get("/")
async def index(request: Request, session_key: Optional[UUID] = Depends(cookie)):
    if(await backend.read(session_id=session_key) is not None):
        return RedirectResponse(app.url_path_for("dashboard"))
    return templates.TemplateResponse("index.html.j2", {"request": request})

@app.get("/dashboard")
async def dashboard(request: Request, session_key: Optional[UUID] = Depends(cookie), data: dict = Depends(static_data), db: Session = Depends(database)):
    session_data = await backend.read(session_id=session_key)
    if(session_data is None):
        return RedirectResponse(app.url_path_for("index"))
    user = get_user(db, session_data.user_id)
    return templates.TemplateResponse("dashboard.html.j2", {
        "request": request, "user": user, "team": user.team.as_dict(),
        "profile_url": session_data.profile_url, 
        "pokemon": data["pokemon"], "items": data["items"],
        "overlay": user.overlay, "arrangements": OverlayConfigs
    })

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    socket_id = uuid4()
    await manager.connect(websocket, client_id, socket_id)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(client_id, socket_id)
