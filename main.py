"""Точка входа в игру «Тамагочи-кликер»."""

from game import constants as cfg
from game.clicker import SimpleRandomClicker
from game.exceptions import GameError, TamagochiIsGone
from game.game import SimpleGame
from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi

ALL_FOOD = [
    Food(name='Бургер', satiety=20, price=40),
    Food(name='Салат', satiety=10, price=20),
    Food(name='Яблоко', satiety=10, price=15),
]
ALL_MEDICINE = [
    Medicine(name='Ибупрофен', price=30, heal_hp=20, number_of_uses=2),
]


def main() -> None:
    """Запустить событийный цикл игры в консоли."""
    tamagochi = SimpleTamagochi()
    clicker = SimpleRandomClicker()
    game = SimpleGame(
        tamagochi, clicker, all_food=ALL_FOOD, all_medicine=ALL_MEDICINE
    )

    print(cfg.WELCOME_MESSAGE)
    output = ''

    while True:
        print('\n'.join((
            cfg.SEPARATOR,
            output,
            cfg.BAG_TEMPLATE.format(food=game.food, medicine=game.medicine),
            cfg.STATUS_TEMPLATE.format(**game.get_status()),
            cfg.SICK_WARNING if game.tamagochi.is_sick() else '',
            cfg.MENU,
        )))
        output = ''
        try:
            match input(cfg.ACTION_PROMPT):
                case '1':
                    output = cfg.WORK_TEMPLATE.format(income=game.work())
                    game.tamagochi.update()
                case '2':
                    game.buy_food()
                    output = cfg.FOOD_BOUGHT_MESSAGE
                case '3':
                    game.buy_medicine()
                    output = cfg.MEDICINE_BOUGHT_MESSAGE
                case '4':
                    game.feed_tamagochi()
                    output = cfg.FED_MESSAGE
                case '5':
                    game.heal_tamagochi()
                    output = cfg.HEALED_MESSAGE
                case '6':
                    game.play_with_tamagochi()
                    output = cfg.PLAYED_MESSAGE
                case '7':
                    game.rest_tamagochi()
                    output = cfg.RESTED_MESSAGE
                case '0':
                    print(cfg.BYE_MESSAGE)
                    break
                case _:
                    output = cfg.UNKNOWN_COMMAND_MESSAGE
        except TamagochiIsGone as error:
            print(error)
            break
        except GameError as error:
            output = str(error)


if __name__ == '__main__':
    main()
