"""Модуль с интерфейсом и реализациями класса кликера."""

import random
from abc import ABC, abstractmethod

from .constants import (
    CLICKER_RANGE_MESSAGE,
    MAX_INCOME_PER_CLICK,
    MIN_INCOME_PER_CLICK,
)


class AbstractClicker(ABC):
    """Интерфейс для кликера."""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации."""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет."""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик.

        :return: количество монет за клик.
        """
        raise NotImplementedError


class SimpleRandomClicker(AbstractClicker):
    """Кликер, который за клик даёт случайное количество монет."""

    def __init__(
        self,
        min_income: int = MIN_INCOME_PER_CLICK,
        max_income: int = MAX_INCOME_PER_CLICK,
    ) -> None:
        """Создать кликер с диапазоном дохода за клик.

        :param min_income: минимальный доход за один клик.
        :param max_income: максимальный доход за один клик.
        :raises ValueError: если диапазон дохода задан некорректно.
        """
        if min_income <= 0 or max_income < min_income:
            raise ValueError(CLICKER_RANGE_MESSAGE)
        self._min_income = min_income
        self._max_income = max_income
        self._income_per_click = 0

    @property
    def income_per_click(self) -> int:
        """Монеты, заработанные за последний клик.

        :return: количество монет, ноль если кликов ещё не было.
        """
        return self._income_per_click

    def click(self) -> None:
        """Заработать случайное количество монет за один клик."""
        self._income_per_click = random.randint(
            self._min_income, self._max_income
        )
