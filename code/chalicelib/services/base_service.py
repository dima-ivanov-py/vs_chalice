from abc import ABCMeta, abstractmethod
from typing import Any, Dict


class BaseService(metaclass=ABCMeta):
    def __init__(self, *, table, data: Dict[str, Any] = None) -> None:
        self._table = table
        self._data = data

    def set_data(self, data: Dict[str, Any]) -> None:
        self._data = data

    def get_table(self):
        return self._table

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def __call__(self) -> Any:
        ...
