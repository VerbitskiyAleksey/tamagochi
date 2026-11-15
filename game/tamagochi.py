"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod

from .exceptions import EmptyMedicine, NotEnoughEnergy, TamagochiIsGone
from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи

        :return: True если тамагочи болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.
        Должен использоваться после каждого взаимодействия с тамагочи
        """
        raise NotImplementedError


class SimpleTamagochi(AbstractTamagochi):
    """
    Питомец с голодом, усталостью, здоровьем и энергией.

    Все показатели лежат в диапазоне 0..100. Каждый тик растут голод
    и усталость, тратится энергия. При критических значениях питомец
    болеет и теряет здоровье, при нулевом здоровье погибает.
    """

    MIN_STAT = 0
    MAX_STAT = 100

    START_HUNGER = 40
    START_FATIGUE = 20
    START_HP = 80
    START_ENERGY = 60

    HUNGER_PER_TICK = 5
    FATIGUE_PER_TICK = 3
    ENERGY_PER_TICK = 2
    SICK_FATIGUE_PER_TICK = 3

    SICK_HUNGER_LIMIT = 70
    SICK_FATIGUE_LIMIT = 80
    CRITICAL_HUNGER = 80
    CRITICAL_FATIGUE = 90

    HUNGER_HP_PENALTY = 10
    FATIGUE_HP_PENALTY = 5
    SICK_HP_PENALTY = 5

    FEED_ENERGY_COST = 5
    PLAY_ENERGY_COST = 15
    PLAY_HUNGER_GAIN = 10
    PLAY_FATIGUE_GAIN = 10
    PLAY_HP_BONUS = 5
    REST_ENERGY_GAIN = 30
    REST_FATIGUE_DROP = 30
    SICK_REST_DIVIDER = 2

    def __init__(self, name: str = 'Бублик') -> None:
        """
        Создать питомца с начальными показателями.

        :param name: имя питомца
        """
        self._name = name
        self._hunger = self.START_HUNGER
        self._fatigue = self.START_FATIGUE
        self._hp = self.START_HP
        self._energy = self.START_ENERGY
        self._sick = False

    @property
    def name(self) -> str:
        """
        Имя питомца.

        :return: имя питомца
        """
        return self._name

    def feed(self, food: Food) -> None:
        """
        Накормить питомца: голод падает, энергия немного тратится.

        :param food: объект еды из сумки игрока
        :raises TamagochiIsGone: если питомец погиб
        """
        self._check_alive()
        self._hunger = self._clamp(self._hunger - food.satiety)
        self._energy = self._clamp(self._energy - self.FEED_ENERGY_COST)

    def play(self) -> None:
        """
        Поиграть с питомцем: энергия и здоровье меняются, голод растёт.

        :raises TamagochiIsGone: если питомец погиб
        :raises NotEnoughEnergy: если энергии не хватает на игру
        """
        self._check_alive()
        if self._energy < self.PLAY_ENERGY_COST:
            raise NotEnoughEnergy(
                'Питомцу не хватает энергии, сначала отдохните'
            )
        self._energy = self._clamp(self._energy - self.PLAY_ENERGY_COST)
        self._hunger = self._clamp(self._hunger + self.PLAY_HUNGER_GAIN)
        self._fatigue = self._clamp(self._fatigue + self.PLAY_FATIGUE_GAIN)
        self._hp = self._clamp(self._hp + self.PLAY_HP_BONUS)

    def rest(self) -> None:
        """
        Отдохнуть: энергия растёт, усталость падает.

        Если питомец болен, отдых действует вдвое слабее.

        :raises TamagochiIsGone: если питомец погиб
        """
        self._check_alive()
        energy_gain = self.REST_ENERGY_GAIN
        fatigue_drop = self.REST_FATIGUE_DROP
        if self._sick:
            energy_gain //= self.SICK_REST_DIVIDER
            fatigue_drop //= self.SICK_REST_DIVIDER
        self._energy = self._clamp(self._energy + energy_gain)
        self._fatigue = self._clamp(self._fatigue - fatigue_drop)

    def heal(self, medicine: Medicine) -> None:
        """
        Вылечить питомца и потратить одно применение лекарства.

        :param medicine: лекарство из сумки игрока
        :raises TamagochiIsGone: если питомец погиб
        :raises EmptyMedicine: если применения лекарства закончились
        """
        self._check_alive()
        if medicine.is_empty():
            raise EmptyMedicine(f'Лекарство «{medicine.name}» закончилось')
        self._hp = self._clamp(self._hp + medicine.heal_hp)
        self._sick = False
        medicine.uses += 1

    @property
    def status(self) -> dict[str, int]:
        """
        Все показатели питомца.

        :return: словарь с ключами hunger, fatigue, hp, energy
        """
        return {
            'hunger': self._hunger,
            'fatigue': self._fatigue,
            'hp': self._hp,
            'energy': self._energy,
        }

    def is_alive(self) -> bool:
        """
        Проверить, жив ли питомец.

        :return: True если здоровье больше нуля, иначе False
        """
        return self._hp > self.MIN_STAT

    def is_sick(self) -> bool:
        """
        Проверить, болен ли питомец.

        :return: True если питомец болеет, иначе False
        """
        return self._sick

    def update(self) -> None:
        """
        Обновить состояние питомца за один тик игры.

        Голод и усталость растут, энергия тратится. При критических
        значениях питомец заболевает и теряет здоровье.
        """
        if not self.is_alive():
            return

        self._hunger = self._clamp(self._hunger + self.HUNGER_PER_TICK)
        fatigue_gain = self.FATIGUE_PER_TICK
        if self._sick:
            fatigue_gain += self.SICK_FATIGUE_PER_TICK
        self._fatigue = self._clamp(self._fatigue + fatigue_gain)
        self._energy = self._clamp(self._energy - self.ENERGY_PER_TICK)

        if (
            self._hunger >= self.SICK_HUNGER_LIMIT
            or self._fatigue >= self.SICK_FATIGUE_LIMIT
        ):
            self._sick = True

        hp_loss = 0
        if self._hunger >= self.CRITICAL_HUNGER:
            hp_loss += self.HUNGER_HP_PENALTY
        if self._fatigue >= self.CRITICAL_FATIGUE:
            hp_loss += self.FATIGUE_HP_PENALTY
        if self._sick:
            hp_loss += self.SICK_HP_PENALTY
        self._hp = self._clamp(self._hp - hp_loss)

    @classmethod
    def _clamp(cls, value: int) -> int:
        """
        Ограничить показатель диапазоном 0..MAX_STAT.

        :param value: новое значение показателя
        :return: значение внутри допустимого диапазона
        """
        return max(cls.MIN_STAT, min(cls.MAX_STAT, value))

    def _check_alive(self) -> None:
        """
        Убедиться, что действие с питомцем ещё возможно.

        :raises TamagochiIsGone: если питомец погиб
        """
        if not self.is_alive():
            raise TamagochiIsGone('Питомец погиб, игра окончена')