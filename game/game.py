"""Модуль с интерфейсом и реализацией класса игры"""

from abc import ABC, abstractmethod
from copy import copy
from typing import Any, TypeVar

from .clicker import AbstractClicker
from .exceptions import (
    EmptyBag,
    EmptyMedicine,
    NotEnoughEnergy,
    NotEnoughMoney,
    TamagochiIsGone,
)
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi

Item = TypeVar('Item', Food, Medicine)


class AbstractGame(ABC):
    """Интерфейс для логики игры"""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа"

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды"""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства"""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
        raise NotImplementedError


class SimpleGame(AbstractGame):
    """Игра с магазином, сумками ресурсов и условием проигрыша."""

    START_COINS = 50

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """
        Создать игру.

        :param tamagochi: питомец, за которым следит игрок
        :param clicker: кликер для заработка монет
        :param all_food: ассортимент еды в магазине
        :param all_medicine: ассортимент лекарств в магазине
        """
        self._tamagochi = tamagochi
        self._clicker = clicker
        self._shop_food = list(all_food)
        self._shop_medicine = list(all_medicine)
        self._food_bag: list[Food] = []
        self._medicine_bag: list[Medicine] = []
        self._coins = self.START_COINS

    @property
    def tamagochi(self) -> AbstractTamagochi:
        """
        Питомец текущей игры.

        :return: питомец
        """
        return self._tamagochi

    @property
    def food(self) -> list[Food]:
        """
        Сумка с едой.

        :return: список купленной еды
        """
        return list(self._food_bag)

    @property
    def medicine(self) -> list[Medicine]:
        """
        Сумка с лекарствами.

        :return: список купленных лекарств
        """
        return list(self._medicine_bag)

    def work(self) -> int:
        """
        Пойти на работу: кликер зарабатывает монеты.

        :return: количество заработанных за ход монет
        """
        self._clicker.click()
        income = self._clicker.income_per_click
        self._coins += income
        return income

    def buy_food(self) -> None:
        """Купить выбранную еду из магазина в сумку."""
        self._buy(self._shop_food, self._food_bag, 'Магазин еды')

    def buy_medicine(self) -> None:
        """Купить выбранное лекарство из магазина в сумку."""
        self._buy(
            self._shop_medicine, self._medicine_bag, 'Магазин лекарств'
        )

    def feed_tamagochi(self) -> None:
        """Покормить питомца выбранной едой из сумки."""
        try:
            food = self._choose_item(self._food_bag, 'Сумка с едой')
            if food is None:
                return
            self._tamagochi.feed(food)
        except (EmptyBag, TamagochiIsGone) as error:
            print(error)
            return
        self._food_bag.remove(food)
        self._tamagochi.update()

    def heal_tamagochi(self) -> None:
        """Вылечить питомца выбранным лекарством из сумки."""
        try:
            medicine = self._choose_item(
                self._medicine_bag, 'Сумка с лекарствами'
            )
            if medicine is None:
                return
            self._tamagochi.heal(medicine)
        except (EmptyBag, EmptyMedicine, TamagochiIsGone) as error:
            print(error)
            return
        if medicine.is_empty():
            self._medicine_bag.remove(medicine)
        self._tamagochi.update()

    def rest_tamagochi(self) -> None:
        """Отдохнуть с питомцем и пропустить один тик."""
        try:
            self._tamagochi.rest()
        except TamagochiIsGone as error:
            print(error)
            return
        self._tamagochi.update()

    def play_with_tamagochi(self) -> None:
        """Поиграть с питомцем и пропустить один тик."""
        try:
            self._tamagochi.play()
        except (NotEnoughEnergy, TamagochiIsGone) as error:
            print(error)
            return
        self._tamagochi.update()

    def get_status(self) -> dict[str, Any]:
        """
        Получить статус игры.

        :return: показатели питомца и ключ coins с количеством монет
        """
        return {**self._tamagochi.status, 'coins': self._coins}

    def is_game_over(self) -> bool:
        """
        Проверить условие конца игры.

        :return: True если питомец погиб, иначе False
        """
        return not self._tamagochi.is_alive()

    def _pay(self, price: int) -> None:
        """
        Списать монеты за покупку.

        :param price: стоимость покупки
        :raises NotEnoughMoney: если монет не хватает
        """
        if price > self._coins:
            raise NotEnoughMoney(
                f'Не хватает монет: нужно {price}, есть {self._coins}'
            )
        self._coins -= price

    def _buy(
        self,
        shop: list[Item],
        bag: list[Item],
        title: str,
    ) -> None:
        """
        Купить предмет из магазина и положить его в сумку.

        :param shop: ассортимент магазина
        :param bag: сумка, в которую попадёт покупка
        :param title: заголовок меню выбора
        """
        try:
            item = self._choose_item(shop, title)
            if item is None:
                return
            self._pay(item.price)
        except (EmptyBag, NotEnoughMoney) as error:
            print(error)
            return
        bag.append(copy(item))
        print(f'Куплено: {item.name} за {item.price} монет')

    @staticmethod
    def _choose_item(items: list[Item], title: str) -> Item | None:
        """
        Показать предметы и вернуть выбранный игроком.

        :param items: список доступных предметов
        :param title: заголовок меню выбора
        :return: выбранный предмет или None при отмене и неверном вводе
        :raises EmptyBag: если список предметов пуст
        """
        if not items:
            raise EmptyBag(f'{title}: пусто, выбирать нечего')
        print(f'\n{title}:')
        for number, item in enumerate(items, start=1):
            print(f'{number}. {item}')
        choice = input('Номер (0 — отмена): ').strip()
        if choice == '0':
            print('Действие отменено')
            return None
        if not choice.isdigit() or not 1 <= int(choice) <= len(items):
            print('Некорректный номер, попробуйте снова')
            return None
        return items[int(choice) - 1]