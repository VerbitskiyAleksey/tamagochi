"""Константы игры: баланс питомца, экономика и тексты интерфейса."""

MIN_INCOME_PER_CLICK = 10
MAX_INCOME_PER_CLICK = 20

START_COINS = 100

MIN_STAT = 0
MAX_STAT = 100

DEFAULT_PET_NAME = 'Бублик'
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

SEPARATOR_WIDTH = 45
SEPARATOR = '=' * SEPARATOR_WIDTH
CANCEL_CHOICE = '0'

WELCOME_MESSAGE = 'Добро пожаловать в тамагочи-кликер!'
BAG_TEMPLATE = 'Сумка с едой: {food}\nСумка с лекарствами: {medicine}'
STATUS_TEMPLATE = (
    'Статус: голод {hunger}, усталость {fatigue}, здоровье {hp}, '
    'энергия {energy}, монет {coins}'
)
SICK_WARNING_LINES = (
    '=======Тамагочи болеет======',
    '=======Отдых действует менее эффективно======',
)
SICK_WARNING = '\n'.join(SICK_WARNING_LINES)

MENU_ITEMS = (
    '1. Пойти на работу',
    '2. Купить еду',
    '3. Купить лекарство',
    '4. Покормить',
    '5. Вылечить',
    '6. Играть',
    '7. Отдых',
    '0. Выход',
)
MENU = '\n'.join(MENU_ITEMS)
ACTION_PROMPT = 'Выберите действие: '
ITEM_PROMPT = 'Номер (0 — отмена): '

SHOP_FOOD_TITLE = 'Магазин еды'
SHOP_MEDICINE_TITLE = 'Магазин лекарств'
FOOD_BAG_TITLE = 'Сумка с едой'
MEDICINE_BAG_TITLE = 'Сумка с лекарствами'

WORK_TEMPLATE = 'Вы заработали {income} монет.'
FOOD_BOUGHT_MESSAGE = 'Еда добавлена в сумку.'
MEDICINE_BOUGHT_MESSAGE = 'Лекарство добавлено в сумку.'
FED_MESSAGE = 'Питомец поел.'
HEALED_MESSAGE = 'Питомец принял лекарство.'
PLAYED_MESSAGE = 'Вы поиграли с питомцем.'
RESTED_MESSAGE = 'Питомец отдохнул.'
UNKNOWN_COMMAND_MESSAGE = 'Неверная команда.'
BYE_MESSAGE = 'До встречи!'

CLICKER_RANGE_MESSAGE = 'Ожидается 0 < min_income <= max_income.'
NOT_ENOUGH_MONEY_TEMPLATE = 'Не хватает монет: нужно {price}, есть {coins}.'
NOT_ENOUGH_ENERGY_MESSAGE = 'Питомцу не хватает энергии, сначала отдохните.'
EMPTY_MEDICINE_TEMPLATE = 'Лекарство «{name}» закончилось.'
EMPTY_BAG_TEMPLATE = '{title}: пусто, выбирать нечего.'
INVALID_CHOICE_MESSAGE = 'Некорректный номер, попробуйте снова.'
ACTION_CANCELLED_MESSAGE = 'Действие отменено.'
PET_IS_GONE_MESSAGE = 'Питомец {name} погиб, игра окончена.'
