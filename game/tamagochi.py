"""Модуль с интерфейсом и реализациями класса тамагочи."""

from abc import ABC, abstractmethod

from . import constants as cfg
from .exceptions import NotEnoughEnergy, TamagochiIsGone
from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """Абстрактный метод для кормления тамагочи.

        :param food: объект еды для кормления.
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """Абстрактный метод для лечения тамагочи.

        :param medicine: лекарство для лечения.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """Абстрактное свойство для доступа ко всем состояниям тамагочи.

        :return: словарь со всеми состояниями тамагочи.
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """Абстрактный метод для проверки жив ли тамагочи.

        :return: True если жив, иначе False.
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """Абстрактный метод для проверки, не заболел ли тамагочи.

        :return: True если тамагочи болеет, иначе False.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """Абстрактный метод для обновления состояний тамагочи.

        Должен использоваться после каждого взаимодействия с тамагочи.
        """
        raise NotImplementedError


class SimpleTamagochi(AbstractTamagochi):
    """Питомец с голодом, усталостью, здоровьем и энергией.

    Показатели лежат в диапазоне от MIN_STAT до MAX_STAT. Каждый тик
    растут голод и усталость, тратится энергия. При критических
    значениях питомец болеет и теряет здоровье, при нулевом здоровье
    погибает.
    """

    def __init__(self, name: str = cfg.DEFAULT_PET_NAME) -> None:
        """Создать питомца с начальными показателями.

        :param name: имя питомца.
        """
        self._name = name
        self._hunger = cfg.START_HUNGER
        self._fatigue = cfg.START_FATIGUE
        self._hp = cfg.START_HP
        self._energy = cfg.START_ENERGY
        self._sick = False

    @property
    def name(self) -> str:
        """Имя питомца.

        :return: имя питомца.
        """
        return self._name

    def feed(self, food: Food) -> None:
        """Накормить питомца: голод падает, энергия немного тратится.

        :param food: объект еды из сумки игрока.
        :raises TamagochiIsGone: если питомец погиб.
        """
        self._check_alive()
        self._hunger = self._clamp(self._hunger - food.satiety)
        self._energy = self._clamp(self._energy - cfg.FEED_ENERGY_COST)

    def play(self) -> None:
        """Поиграть с питомцем: энергия тратится, голод и усталость растут.

        :raises TamagochiIsGone: если питомец погиб.
        :raises NotEnoughEnergy: если энергии не хватает на игру.
        """
        self._check_alive()
        if self._energy < cfg.PLAY_ENERGY_COST:
            raise NotEnoughEnergy(cfg.NOT_ENOUGH_ENERGY_MESSAGE)
        self._energy = self._clamp(self._energy - cfg.PLAY_ENERGY_COST)
        self._hunger = self._clamp(self._hunger + cfg.PLAY_HUNGER_GAIN)
        self._fatigue = self._clamp(self._fatigue + cfg.PLAY_FATIGUE_GAIN)
        self._hp = self._clamp(self._hp + cfg.PLAY_HP_BONUS)

    def rest(self) -> None:
        """Отдохнуть: энергия растёт, усталость падает.

        Если питомец болен, отдых действует вдвое слабее.

        :raises TamagochiIsGone: если питомец погиб.
        """
        self._check_alive()
        energy_gain = cfg.REST_ENERGY_GAIN
        fatigue_drop = cfg.REST_FATIGUE_DROP
        if self._sick:
            energy_gain //= cfg.SICK_REST_DIVIDER
            fatigue_drop //= cfg.SICK_REST_DIVIDER
        self._energy = self._clamp(self._energy + energy_gain)
        self._fatigue = self._clamp(self._fatigue - fatigue_drop)

    def heal(self, medicine: Medicine) -> None:
        """Вылечить питомца лекарством.

        :param medicine: лекарство из сумки игрока.
        :raises TamagochiIsGone: если питомец погиб.
        :raises EmptyMedicine: если применения лекарства закончились.
        """
        self._check_alive()
        medicine.use()
        self._hp = self._clamp(self._hp + medicine.heal_hp)
        self._sick = False

    @property
    def status(self) -> dict[str, int]:
        """Все показатели питомца.

        :return: словарь с ключами hunger, fatigue, hp, energy.
        """
        return {
            'hunger': self._hunger,
            'fatigue': self._fatigue,
            'hp': self._hp,
            'energy': self._energy,
        }

    def is_alive(self) -> bool:
        """Проверить, жив ли питомец.

        :return: True если здоровье больше нуля, иначе False.
        """
        return self._hp > cfg.MIN_STAT

    def is_sick(self) -> bool:
        """Проверить, болен ли питомец.

        :return: True если питомец болеет, иначе False.
        """
        return self._sick

    def update(self) -> None:
        """Обновить состояние питомца за один тик игры.

        :raises TamagochiIsGone: если питомец уже погиб.
        """
        self._check_alive()
        self._hunger = self._clamp(self._hunger + cfg.HUNGER_PER_TICK)
        fatigue_gain = cfg.FATIGUE_PER_TICK
        if self._sick:
            fatigue_gain += cfg.SICK_FATIGUE_PER_TICK
        self._fatigue = self._clamp(self._fatigue + fatigue_gain)
        self._energy = self._clamp(self._energy - cfg.ENERGY_PER_TICK)
        self._update_sickness()
        self._hp = self._clamp(self._hp - self._hp_loss())

    def _update_sickness(self) -> None:
        """Заболеть, если голод или усталость превысили пороги."""
        if (
            self._hunger >= cfg.SICK_HUNGER_LIMIT
            or self._fatigue >= cfg.SICK_FATIGUE_LIMIT
        ):
            self._sick = True

    def _hp_loss(self) -> int:
        """Посчитать потерю здоровья за тик.

        :return: сумма штрафов за голод, усталость и болезнь.
        """
        loss = 0
        if self._hunger >= cfg.CRITICAL_HUNGER:
            loss += cfg.HUNGER_HP_PENALTY
        if self._fatigue >= cfg.CRITICAL_FATIGUE:
            loss += cfg.FATIGUE_HP_PENALTY
        if self._sick:
            loss += cfg.SICK_HP_PENALTY
        return loss

    @staticmethod
    def _clamp(value: int) -> int:
        """Ограничить показатель диапазоном MIN_STAT..MAX_STAT.

        :param value: новое значение показателя.
        :return: значение внутри допустимого диапазона.
        """
        return max(cfg.MIN_STAT, min(cfg.MAX_STAT, value))

    def _check_alive(self) -> None:
        """Убедиться, что действие с питомцем ещё возможно.

        :raises TamagochiIsGone: если питомец погиб.
        """
        if not self.is_alive():
            raise TamagochiIsGone(
                cfg.PET_IS_GONE_MESSAGE.format(name=self._name)
            )
