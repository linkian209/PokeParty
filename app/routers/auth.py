from app.db import create_user, get_user, database
from app.session import SessionData, backend, cookie, verifier
from app.settings import Settings
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from requests_oauthlib import OAuth2Session
from sqlalchemy.orm import Session
from uuid import uuid4, UUID

router = APIRouter(prefix="/auth", tags=["auth"])
settings = Settings()

OAUTH_BASE_URL = "https://id.twitch.tv/oauth2"
AUTH_URL = OAUTH_BASE_URL + "/authorize"
TOKEN_URL = OAUTH_BASE_URL + "/token"
WHOAMI_API = "https://api.twitch.tv/helix/users"

@router.get("/login")
async def login(request: Request):
    twitch = OAuth2Session(settings.client_id, scope=[], redirect_uri=settings.callback_url)
    authorization_url, state = twitch.authorization_url(AUTH_URL)
    response = RedirectResponse(authorization_url)
    
    session_key = uuid4()
    data = SessionData(oauth_state=state)
    await backend.create(session_key, data)
    cookie.attach_to_response(response=response, session_id=session_key)
    
    return response

@router.get("/callback", dependencies=[Depends(cookie)], response_class=RedirectResponse)
async def callback(request: Request, session_data: SessionData = Depends(verifier), session_key: UUID = Depends(cookie), db: Session = Depends(database)):
    twitch = OAuth2Session(
        settings.client_id, state=session_data.oauth_state, redirect_uri=settings.callback_url
    )
    token = twitch.fetch_token(
        token_url=TOKEN_URL, include_client_id=True,
        client_secret=settings.client_secret, authorization_response=str(request.url)
    )
    user_data = twitch.get(
        WHOAMI_API, headers={"Client-ID": settings.client_id, "Authorization": f"Bearer {token['access_token']}"}
    ).json()["data"][0]

    user = get_user(db, user_data["id"])
    if(user is None):
        user = create_user(db, user_id=user_data["id"], username=user_data["display_name"])

    session_data.user_id = user.id
    session_data.access_token = token["access_token"]
    session_data.profile_url = user_data['profile_image_url']
    session_data.refresh_token = token['refresh_token']

    await backend.update(session_id=session_key, data=session_data)

    return request.url_for("dashboard")

@router.get("/logout", name="logout", dependencies=[Depends(cookie)], response_class=RedirectResponse)
async def logout(request: Request, response: Response, session_key: UUID = Depends(cookie)):
    await backend.delete(session_key)
    cookie.delete_from_response(response)
    return request.url_for("index")