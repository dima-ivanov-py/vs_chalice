import os

import boto3


class TableGetter:
    def __init__(self, *, env_name: str) -> None:
        self.env_name = env_name
        self.table = None

    def _get_table(self):
        return boto3.resource("dynamodb").Table(os.environ[self.env_name])

    def __call__(self):
        if self.table is None:
            self.table = self._get_table()
        return self.table
