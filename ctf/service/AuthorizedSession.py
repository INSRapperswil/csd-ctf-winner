import requests
import logging as log
from datetime import datetime
from datetime import timedelta
from typing import Dict

from requests.models import Response


class AuthorizedSession:
    def __init__(self, tenant: str, username: str, password: str) -> None:
        self.tenant = tenant
        self.username = username
        self.password = password
        self._reset_tokens()

    def get(self, path: str) -> Response:
        self._ensure_login()
        url = f"https://{self.tenant}.hacking-lab.com/{path}"
        response = requests.get(
            url, headers={"Authorization": f"Bearer {self._access_token}"}
        )
        return response

    def logout(self) -> bool:
        log.info("logout")
        try:
            logout_request = requests.post(
                f"https://auth.{self.tenant}-dc.hacking-lab.com/auth/realms/{self.tenant}/protocol/openid-connect/logout/",
                data={
                    "client_id": "ccs",
                    "refresh_token": self._refresh_token,
                },
            )
            logout_request.raise_for_status()
            self._reset_tokens()
        except requests.exceptions.HTTPError:
            return False
        return True

    def _reset_tokens(self) -> None:
        self._access_token = None
        self._refresh_token = None
        self._access_expires_at = datetime.now() - timedelta(weeks=1)
        self._refresh_expires_at = datetime.now() - timedelta(weeks=1)

    def _authorize(self) -> bool:
        log.info("_authorize")
        return self._token(
            {
                "username": self.username,
                "password": self.password,
                "grant_type": "password",
                "client_id": "ccs",
            }
        )

    def _refresh(self) -> None:
        log.info("_refresh")
        return self._token(
            {
                "grant_type": "refresh_token",
                "client_id": "ccs",
                "refresh_token": self._refresh_token,
            }
        )

    def _token(self, data: Dict) -> bool:
        try:
            token_request = requests.post(
                f"https://auth.{self.tenant}-dc.hacking-lab.com/auth/realms/{self.tenant}/protocol/openid-connect/token/",
                data=data,
            )
            token_request.raise_for_status()
            token_json = token_request.json()
            self._access_token = token_json["access_token"]
            self._refresh_token = token_json["refresh_token"]
            self._access_expires_at = datetime.now() + timedelta(
                seconds=token_json["expires_in"]
            )
            self._refresh_expires_at = datetime.now() + timedelta(
                seconds=token_json["refresh_expires_in"]
            )
        except requests.exceptions.HTTPError:
            return False
        return True

    def _ensure_login(self) -> bool:
        if datetime.now() >= self._refresh_expires_at:
            log.info("refresh token expired")
            return self._authorize()
        elif datetime.now() >= self._access_expires_at:
            log.info("access token expired")
            return self._refresh()

    def __enter__(self):
        self._ensure_login()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.logout()
