"""Модуль с интерфейсом и реализациями класса кликера"""

import random
from abc import ABC, abstractmethod


class AbstractClicker(ABC):
    """Интерфейс для кликера"""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации"""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет"""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик"""
        raise NotImplementedError


class SimpleRandomClicker(AbstractClicker):
    """Кликер, который за клик даёт случайное количество монет."""

    def __init__(self, min_income: 10, max_income: 20) -> None:
        """
        Создать кликер с диапазоном дохода за клик.

        :param min_income: минимальный доход за один клик
        :param max_income: максимальный доход за один клик
        :raises ValueError: если диапазон дохода задан некорректно
        """
        if min_income <= 0 or max_income < min_income:
            raise ValueError('Ожидается 0 < min_income <= max_income')
        self._min_income = min_income
        self._max_income = max_income
        self._income_per_click = 0

    @property
    def income_per_click(self) -> int:
        """
        Монеты, заработанные за последний клик.

        :return: количество монет, 0 если кликов ещё не было
        """
        return self._income_per_click

    def click(self) -> None:
        """Заработать случайное количество монет за один клик."""
        self._income_per_click = random.randint(
            self._min_income, self._max_income
        )