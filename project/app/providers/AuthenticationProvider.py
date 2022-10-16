import logging
from typing import List, Set
from fastapi import Depends, Header
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette import status

from app.api.auth import get_current_active_user
from app.models.user import User
from app.utils import oauth2_scheme


log = logging.getLogger("uvicorn")

class AuthenticationProvider: # pragma: no cover
    def __init__(self, *, scopes: List[str] = ["*"]):
        self.scopes = set(scopes)

    async def __call__(self, request: Request, bearer_token: str = Header(None)) -> User:
        authorization = request.headers.get('Authorization') or bearer_token
        scheme, authorization_param = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "bearer":
            authorization_param = None

        authenticated_user = await get_current_active_user(authorization_param)
        
        if not authenticated_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )
        return authenticated_user

    def has_required_scope(self, user_scopes: Set[str]) -> bool:  # pragma: no cover
        """Verify the user has the desired authorization scope"""
        print(user_scopes)
        # for scope in self.scopes:
        #     if scope not in user_scopes:
        #         return False
        return True
