"""Модуль с моделями игры (еда, лекарство)."""

from dataclasses import dataclass

from .constants import EMPTY_MEDICINE_TEMPLATE
from .exceptions import EmptyMedicine


@dataclass(frozen=True, slots=True)
class Food:
    """Модель объекта еды."""

    name: str
    satiety: int
    price: int

    def __repr__(self) -> str:
        """Вернуть читаемое описание еды.

        :return: строка с названием, ценой и насыщением.
        """
        return (
            f'{self.name} стоимость: {self.price}, '
            f'утоляет голод на {self.satiety} единиц'
        )


@dataclass
class Medicine:
    """Модель объекта лекарства."""

    name: str
    price: int
    heal_hp: int
    number_of_uses: int
    uses: int = 0

    def is_empty(self) -> bool:
        """Проверить, закончились ли применения лекарства.

        :return: True если применений не осталось, иначе False.
        """
        return self.uses >= self.number_of_uses

    def use(self) -> None:
        """Применить лекарство один раз.

        :raises EmptyMedicine: если применения лекарства закончились.
        """
        if self.is_empty():
            raise EmptyMedicine(
                EMPTY_MEDICINE_TEMPLATE.format(name=self.name)
            )
        self.uses += 1

    def __repr__(self) -> str:
        """Вернуть читаемое описание лекарства.

        :return: строка с названием, ценой и остатком применений.
        """
        left = self.number_of_uses - self.uses
        return (
            f'{self.name} стоимость: {self.price}, '
            f'лечит на {self.heal_hp} HP, '
            f'использований: {left}/{self.number_of_uses}'
        )
