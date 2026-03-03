from abc import ABC, abstractmethod
from typing import Any, Dict


class Configuration(ABC):
    def __init__(self, **kwargs: Any):
        """Инициализация конфигурации с динамическими атрибутами

        Args:
            kwargs (dict): Словарь с атрибутами
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Конвертация

        Returns:
            dict
        """
        pass
