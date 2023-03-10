from app.db import User
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi import HTTPException
from uuid import UUID
from pydantic import BaseModel


class SessionData(BaseModel):
    user_id: int | None
    oauth_state: str
    profile_url: str | None
    access_token: str | None
    refresh_token: str | None

    class Config:
        arbitrary_types_allowed = True


cookie_params = CookieParameters()

cookie = SessionCookie(
    cookie_name="pokeparty", identifier="general_identifier", auto_error=False,
    secret_key="TODO", cookie_params=cookie_params
)

backend = InMemoryBackend[UUID, SessionData]()

class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
        self, *, identifier: str, auto_error: bool, 
        backend: InMemoryBackend[UUID, SessionData], 
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True


verifier = BasicVerifier(
    identifier="general_identifier", auto_error=True, backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session")
)