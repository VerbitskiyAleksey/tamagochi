"""Модуль с исключениями игры."""


class GameError(Exception):
    """Базовая ошибка игры."""


class TamagochiIsGone(GameError):
    """Ошибка при смерти тамагочи."""


class NotEnoughMoney(GameError):
    """Ошибка когда не хватает монет для покупки."""


class NotEnoughEnergy(GameError):
    """Ошибка когда тамагочи не хватает энергии для действия."""


class EmptyMedicine(GameError):
    """Ошибка когда лекарство полностью израсходовано."""


class EmptyBag(GameError):
    """Ошибка когда в сумке или магазине нет предметов."""


class InvalidChoice(GameError):
    """Ошибка когда игрок ввёл неверный номер предмета."""


class ActionCancelled(GameError):
    """Ошибка когда игрок отменил выбор предмета."""
