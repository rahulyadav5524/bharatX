import base64
import json

from app.access_control.schema import BasicAuthCredentials
from config import Config


class AuthenticationService:
    __config: dict = {}

    @classmethod
    def set_config(cls):
        AuthenticationService.__config = Config.AUTH

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

    def get_basic_auth_credentials(
        self, encoded_str: str
    ) -> tuple[BasicAuthCredentials | None, str | None]:
        if not encoded_str:
            return None, "No credentials provided"
        try:
            username, password = self.decode_basic_auth(encoded_str)
            return BasicAuthCredentials(username=username, password=password), None
        except Exception as e:
            return None, f"Invalid credentials format: {str(e)}"

    def decode_basic_auth(self, encoded_str: str) -> tuple[str, str]:
        try:
            decoded_bytes = base64.b64decode(encoded_str)
            decoded_str = decoded_bytes.decode("utf-8")
            username, password = decoded_str.split(":", 1)
            return username, password
        except (ValueError, UnicodeDecodeError) as e:
            raise ValueError(f"Invalid basic auth format: {str(e)}")
