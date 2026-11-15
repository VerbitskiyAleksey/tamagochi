"""Модуль с исключениями"""


class TamagochiIsGone(Exception):
    """Ошибка при смерти тамагочи"""


class NotEnoughMoney(Exception):
    """Ошибка когда не хватает монет для покупки"""


class NotEnoughEnergy(Exception):
    """Ошибка когда тамагочи не хватает энергии для действия"""


class EmptyMedicine(Exception):
    """Ошибка когда лекарство полностью израсходовано"""


class EmptyBag(Exception):
    """Ошибка когда в сумке или магазине нет предметов"""