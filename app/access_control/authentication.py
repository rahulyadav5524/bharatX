import json
from typing import Optional, Tuple
from basicauth import decode

from app.access_control.schema import BasicAuthCredentials
from config import Config


class AuthenticationService:
    __config: dict = {}

    @classmethod
    def set_config(cls):
        AuthenticationService.__config = json.loads(Config.AUTH)

    @classmethod
    def basic_auth(self, encoded_str: str) -> bool:
        creds, error = self.get_basic_auth_credentials(encoded_str)
        if error:
            return False

        username = creds.username
        password = creds.password

        users = AuthenticationService.__config.get("users", None)

        if users is None or users.get(username, None) is None:
            return False
        if users[username] == password:
            return True
        return False

    @classmethod
    def get_basic_auth_credentials(
        cls, encoded_str: str
    ) -> Tuple[Optional[BasicAuthCredentials], Optional[str]]:
        try:
            username, password = decode(encoded_str)
        except Exception as err:
            return None, repr(err)
        return BasicAuthCredentials(username=username, password=password), None
