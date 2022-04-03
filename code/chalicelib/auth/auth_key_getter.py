import base64

import boto3
from chalicelib.config import SSM_AUTH_KEY_PARAM_NAME


class AuthKeyGetter:
    def __init__(self) -> None:
        self.auth_key = None

    @staticmethod
    def _get_auth_key():
        base64_key = boto3.client("ssm").get_parameter(
            Name=SSM_AUTH_KEY_PARAM_NAME, WithDecryption=True
        )["Parameter"]["Value"]
        return base64.b64decode(base64_key)

    def __call__(self):
        if self.auth_key is None:
            self.auth_key = self._get_auth_key()
        return self.auth_key


get_auth_key = AuthKeyGetter()
