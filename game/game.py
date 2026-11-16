"""Модуль с интерфейсом и реализацией класса игры."""

from abc import ABC, abstractmethod
from copy import copy
from typing import Any, TypeVar

from . import constants as cfg
from .clicker import AbstractClicker
from .exceptions import (
    ActionCancelled,
    EmptyBag,
    InvalidChoice,
    NotEnoughMoney,
)
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi

Item = TypeVar('Item', Food, Medicine)


class AbstractGame(ABC):
    """Интерфейс для логики игры."""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """Абстрактный метод инициализации класса игры.

        :param tamagochi: экземпляр тамагочи.
        :param clicker: экземпляр кликера.
        :param all_food: все доступные варианты еды.
        :param all_medicine: все доступные варианты лекарств.
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """Абстрактный метод для логики действия «работа».

        :return: количество заработанных монет.
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """Абстрактный метод для получения статуса тамагочи.

        :return: словарь со всеми характеристиками тамагочи.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """Абстрактное свойство для доступа к сумке с едой.

        :return: список с имеющимися объектами еды.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """Абстрактное свойство для доступа к сумке с лекарствами.

        :return: список с имеющимися объектами лекарств.
        """
        raise NotImplementedError


class SimpleGame(AbstractGame):
    """Игра с магазином, сумками ресурсов и менеджментом монет."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """Создать игру.

        :param tamagochi: питомец, за которым следит игрок.
        :param clicker: кликер для заработка монет.
        :param all_food: ассортимент еды в магазине.
        :param all_medicine: ассортимент лекарств в магазине.
        """
        self._tamagochi = tamagochi
        self._clicker = clicker
        self._shop_food = list(all_food)
        self._shop_medicine = list(all_medicine)
        self._food_bag: list[Food] = []
        self._medicine_bag: list[Medicine] = []
        self._coins = cfg.START_COINS

    @property
    def tamagochi(self) -> AbstractTamagochi:
        """Питомец текущей игры.

        :return: питомец.
        """
        return self._tamagochi

    @property
    def food(self) -> list[Food]:
        """Сумка с едой.

        :return: список купленной еды.
        """
        return list(self._food_bag)

    @property
    def medicine(self) -> list[Medicine]:
        """Сумка с лекарствами.

        :return: список купленных лекарств.
        """
        return list(self._medicine_bag)

    def work(self) -> int:
        """Пойти на работу: кликер зарабатывает монеты.

        :return: количество заработанных за ход монет.
        """
        self._clicker.click()
        income = self._clicker.income_per_click
        self._coins += income
        return income

    def buy_food(self) -> None:
        """Купить выбранную еду из магазина в сумку.

        :raises EmptyBag: если магазин пуст.
        :raises InvalidChoice: если номер предмета неверный.
        :raises ActionCancelled: если игрок отменил выбор.
        :raises NotEnoughMoney: если монет не хватает.
        """
        self._buy(self._shop_food, self._food_bag, cfg.SHOP_FOOD_TITLE)

    def buy_medicine(self) -> None:
        """Купить выбранное лекарство из магазина в сумку.

        :raises EmptyBag: если магазин пуст.
        :raises InvalidChoice: если номер предмета неверный.
        :raises ActionCancelled: если игрок отменил выбор.
        :raises NotEnoughMoney: если монет не хватает.
        """
        self._buy(
            self._shop_medicine, self._medicine_bag, cfg.SHOP_MEDICINE_TITLE
        )

    def feed_tamagochi(self) -> None:
        """Покормить питомца выбранной едой из сумки.

        :raises EmptyBag: если сумка пуста.
        :raises InvalidChoice: если номер предмета неверный.
        :raises ActionCancelled: если игрок отменил выбор.
        :raises TamagochiIsGone: если питомец погиб.
        """
        food = self._choose_item(self._food_bag, cfg.FOOD_BAG_TITLE)
        self._tamagochi.feed(food)
        self._food_bag.remove(food)
        self._tamagochi.update()

    def heal_tamagochi(self) -> None:
        """Вылечить питомца выбранным лекарством из сумки.

        :raises EmptyBag: если сумка пуста.
        :raises InvalidChoice: если номер предмета неверный.
        :raises ActionCancelled: если игрок отменил выбор.
        :raises EmptyMedicine: если применения лекарства закончились.
        :raises TamagochiIsGone: если питомец погиб.
        """
        medicine = self._choose_item(
            self._medicine_bag, cfg.MEDICINE_BAG_TITLE
        )
        self._tamagochi.heal(medicine)
        if medicine.is_empty():
            self._medicine_bag.remove(medicine)
        self._tamagochi.update()

    def rest_tamagochi(self) -> None:
        """Отдохнуть с питомцем и пропустить один тик.

        :raises TamagochiIsGone: если питомец погиб.
        """
        self._tamagochi.rest()
        self._tamagochi.update()

    def play_with_tamagochi(self) -> None:
        """Поиграть с питомцем и пропустить один тик.

        :raises NotEnoughEnergy: если энергии не хватает на игру.
        :raises TamagochiIsGone: если питомец погиб.
        """
        self._tamagochi.play()
        self._tamagochi.update()

    def get_status(self) -> dict[str, Any]:
        """Получить статус игры.

        :return: показатели питомца и ключ coins с количеством монет.
        """
        return {**self._tamagochi.status, 'coins': self._coins}

    def _pay(self, price: int) -> None:
        """Списать монеты за покупку.

        :param price: стоимость покупки.
        :raises NotEnoughMoney: если монет не хватает.
        """
        if price > self._coins:
            raise NotEnoughMoney(
                cfg.NOT_ENOUGH_MONEY_TEMPLATE.format(
                    price=price, coins=self._coins
                )
            )
        self._coins -= price

    def _buy(
        self,
        shop: list[Item],
        bag: list[Item],
        title: str,
    ) -> None:
        """Купить предмет из магазина и положить его в сумку.

        :param shop: ассортимент магазина.
        :param bag: сумка, в которую попадёт покупка.
        :param title: заголовок меню выбора.
        :raises NotEnoughMoney: если монет не хватает.
        """
        item = self._choose_item(shop, title)
        self._pay(item.price)
        bag.append(copy(item))

    @staticmethod
    def _choose_item(items: list[Item], title: str) -> Item:
        """Показать предметы и вернуть выбранный игроком.

        :param items: список доступных предметов.
        :param title: заголовок меню выбора.
        :return: выбранный предмет.
        :raises EmptyBag: если список предметов пуст.
        :raises ActionCancelled: если игрок отменил выбор.
        :raises InvalidChoice: если введён неверный номер.
        """
        if not items:
            raise EmptyBag(cfg.EMPTY_BAG_TEMPLATE.format(title=title))
        print(f'\n{title}:')
        for number, item in enumerate(items, start=1):
            print(f'{number}. {item}')
        choice = input(cfg.ITEM_PROMPT).strip()
        if choice == cfg.CANCEL_CHOICE:
            raise ActionCancelled(cfg.ACTION_CANCELLED_MESSAGE)
        if not choice.isdigit() or not 1 <= int(choice) <= len(items):
            raise InvalidChoice(cfg.INVALID_CHOICE_MESSAGE)
        return items[int(choice) - 1]
