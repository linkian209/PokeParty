from app.session import SessionData, cookie, verifier
from app.db import Team, database, get_user, get_overlay, OverlayConfigs
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter(prefix="/overlay", tags=["overlay"])
templates = Jinja2Templates(directory="templates")

class OverlayUpdate(BaseModel):
    width: int
    height: int
    arrangement: OverlayConfigs
    outline: bool

@router.post("/", dependencies=[Depends(cookie)])
def update_overlay(update: OverlayUpdate, session_data: SessionData = Depends(verifier), db: Session = Depends(database)):
    user = get_user(db, session_data.user_id)
    user.overlay.width = update.width
    user.overlay.height = update.height
    user.overlay.arrangement = update.arrangement
    user.overlay.outline_items = update.outline
    db.commit()


def make_overlay_response(team: Team, width: int, height: int, rows: int, columns: int, outline: bool, request: Request, overlay_id: int) -> Response:
    layout = []
    cur_row = []
    cur_col = 0

    for i in range(6):
        if cur_col >= columns:
            layout.append(cur_row)
            cur_row = []
            cur_col = 0
        pokemon = getattr(team, f"pokemon{i+1}")
        item = getattr(team, f"item{i+1}")
        cur_row.append({
            "pokemon": pokemon if pokemon else "",
            "item": item if item else "",
            "index": i+1
        })
        cur_col += 1
    layout.append(cur_row)

    return templates.TemplateResponse("overlay.html.j2", {
        "request": request, "width": width, "height": height,
        "id": overlay_id, "layout": layout, "outline": outline,
        "client_id": team.user_id
    })

@router.get("/preview/{overlay_id}")
def preview_overlay(request: Request, overlay_id: str, width: int | None, height: int | None, arrangement: OverlayConfigs | None, outline: bool | None, db: Session = Depends(database)):
    overlay = get_overlay(db, overlay_id=overlay_id)
    if(overlay is None):
        raise HTTPException(status_code=404, detail="Overlay not found")

    width = overlay.width if width is None else int(width)
    height = overlay.height if height is None else int(height)
    outline = overlay.outline_items if outline is None else bool(int(outline))
    rows, cols = overlay.arrangement.value.split('x') if arrangement is None else arrangement.value.split('x')

    return make_overlay_response(team=overlay.user.team, width=width, height=height, rows=int(rows), columns=int(cols), outline=outline, request=request, overlay_id=overlay.id)

@router.get("/{overlay_id}")
def overlay(request: Request, overlay_id: str, db: Session = Depends(database)):
    overlay = get_overlay(db, overlay_id=overlay_id)
    if(overlay is None):
        raise HTTPException(status_code=404, detail="Overlay not found")

    rows, cols = overlay.arrangement.value.split('x')

    return make_overlay_response(team=overlay.user.team, width=overlay.width, height=overlay.height, rows=int(rows), columns=int(cols), outline=overlay.outline_items, request=request, overlay_id=overlay_id)