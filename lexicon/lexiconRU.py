from database import db, getFromTable

lexRU = {\
    'message': {
        'adminStart': '<b>Здравствуйте, администратор!</b>\n\nЧтобы редактировать бота, воспользуйтесь кнопками ниже',
        'moderStart': '<b>Здравствуйте, модератор!</b>\n\nЧтобы редактировать бота, воспользуйтесь кнопками ниже',
        'userStart': '<b>Добро пожаловать в Adidas Shop!</b>\n\nЧтобы приступить к покупкам, перейдите в каталог\n\nПо всем вопросам пишите к нам в чат @shtankomedia',
        'moderator': '<b>Список модераторов:</b>\n\n<tg-spoiler>Чтобы удалить модератора, нажмите на него</tg-spoiler>',
        'addModerator': 'Введите @username модератора, которого хотите добавить',
        'catalog': '<b>Каталог магазина AdidasShop:</b>',
        'database': '<b>База данных пользователей:</b>',
        'orders': '<b>Вот ваши заказы:</b>',
        'noOrders': '<b>Пока что заказы отсутствуют</b>',
        'categoryName': 'Введите имя категории',
        'categoryAdded': '<b>Категория добавлена</b>\n\nЧтобы редактировать бота, воспользуйтесь кнопками ниже',
        'askName': 'Введите имя',
        'askDescription': 'Введите описание',
        'askPrice': 'Введите цену',
        'askPhoto': 'Пришлите одно фото',
        'successModer': '<b>Действие успешно выполнено!</b>\n\nЧтобы редактировать бота, воспользуйтесь кнопками ниже',
        'failModer': '<b>Действие было отменено!</b>\n\nЧтобы редактировать бота, воспользуйтесь кнопками ниже',
        'successUser': '<b>Действие успешно выполнено!</b>\n\nЧтобы продолжить, воспользуйтесь кнопками ниже',
        'failUser': '<b>Действие было отменено!</b>\n\nЧтобы продолжить, воспользуйтесь кнопками ниже',
        'areSure': '<b>Вы уверены?</b>',
        'irregularData': 'Введите корректные данные',
        'else': '<b>Извините, но я не понимаю вас</b>\n\nВоспользуйтесь предложенными командами'
    },
    'images': {
        'logo': 'AgACAgIAAxkBAAIBVGh7TJqsg5zb45R-QrszkkcQf_NeAAJK_zEblRjZS2z_xnVkVNgnAQADAgADcwADNgQ' 
    },
    'button': {
        'moderator': 'Модераторы',
        'catalog': 'Каталог',
        'orders': 'Заказы',
        'database': 'База данных',
        'add': 'Добавить',
        'delete': 'Удалить',
        'clear': 'Очистить',
        'addCategory': 'Добавить категорию',
        'addProduct': 'Добавить продукт',
        'buy': 'Купить',
        'yes': '✅',
        'no': '❌',
        'cancel': '⏪ Назад'
    }
}

def loadProduct(toDisplay: list) -> str:
    return f'<b>{toDisplay[0]}</b>\n\n{toDisplay[1]}\n\nЦена: {toDisplay[2]} рублей'

def getDatabase() -> str:
    text: str = lexRU['message']['database'] + '\n\n'
    for username in [row[1] for row in getFromTable('utils')]:
        text += (username + '\n')
    return text

def getOrders() -> str:
    text = lexRU['message']['orders'] + '\n\n'
    for username, things in db['orders'].items():
        for thing in things:
            text += f'{username} заказал "{thing}"\n'
    return text