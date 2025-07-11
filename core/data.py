masters = [
    {"id": 1, "name": "Сэр Уинстон Черчилль", "experience": 12},
    {"id": 2, "name": "Лорд Байрон", "experience": 8},
    {"id": 3, "name": "Герцог Веллингтон", "experience": 15},
    {"id": 4, "name": "Леди Ада Ловелас", "experience": 7},
    {"id": 5, "name": "Сэр Артур Конан Дойл", "experience": 10}
]


# Список возможных услуг барбершопа
services = [
    {"name": "Королевское Бритье", "price": 1500, "icon": "crown"},
    {"name": "Джентльменская Стрижка", "price": 1200, "icon": "scissors"},
    {"name": "Уход за Бородой", "price": 900, "icon": "brush"},
    {"name": "Аристократическая Укладка", "price": 800, "icon": "star"},
    {"name": "Церемония Очищения", "price": 700, "icon": "cloud-drizzle"},
    {"name": "Реставрация Волос", "price": 1800, "icon": "gem"},
    {"name": "Ночной Дозор", "price": 1000, "icon": "moon"},
    {"name": "Восковая Печать", "price": 600, "icon": "seal"}
]

# Статусы заявок
STATUS_NEW = 'новая'
STATUS_CONFIRMED = 'подтвержденная'
STATUS_CANCELLED = 'отмененная'
STATUS_COMPLETED = 'выполненная'

# Тестовые данные заявок
orders = [
    {
        "id": 1,
        "client_name": "Пётр 'Безголовый' Головин",
        "services": ["Стрижка под 'Горшок'", "Полировка лысины до блеска"],
        "master_id": 1,
        "date": "2025-03-20",
        "status": STATUS_NEW
    },
    {
        "id": 2,
        "client_name": "Василий 'Кудрявый' Прямиков",
        "services": ["Укладка 'Взрыв на макаронной фабрике'"],
        "master_id": 2,
        "date": "2025-03-21",
        "status": STATUS_CONFIRMED
    },
    {
        "id": 3,
        "client_name": "Афанасий 'Бородач' Бритвенников",
        "services": ["Королевское бритье опасной бритвой", "Стрижка бороды 'Боярин'", "Массаж головы 'Озарение'"],
        "master_id": 3,
        "date": "2025-03-19",
        "status": STATUS_COMPLETED
    },
    {
        "id": 4,
        "client_name": "Зинаида 'Радуга' Красильникова",
        "services": ["Окрашивание 'Жизнь в розовом цвете'", "Укладка 'Ветер в голове'"],
        "master_id": 4,
        "date": "2025-03-22",
        "status": STATUS_CANCELLED
    },
    {
        "id": 5,
        "client_name": "Олег 'Викинг' Рюрикович",
        "services": ["Плетение косичек 'Викинг'", "Стрижка бороды 'Боярин'"],
        "master_id": 5,
        "date": "2025-03-23",
        "status": STATUS_NEW
    },
    {
        "id": 6,
        "client_name": "Геннадий 'Блестящий' Лысенко",
        "services": ["Полировка лысины до блеска", "Массаж головы 'Озарение'"],
        "master_id": 1,
        "date": "2025-03-24",
        "status": STATUS_CONFIRMED
    },
    {
        "id": 7,
        "client_name": "Марина 'Рапунцель' Косичкина",
        "services": ["Укладка 'Ветер в голове'", "Мытье головы 'Душ впечатлений'"],
        "master_id": 2,
        "date": "2025-03-25",
        "status": STATUS_CANCELLED
    },
    {
        "id": 8,
        "client_name": "Федор 'Кучерявый' Завитушкин",
        "services": ["Укладка 'Взрыв на макаронной фабрике'", "Массаж головы 'Озарение'", "Мытье головы 'Душ впечатлений'"],
        "master_id": 3,
        "date": "2025-03-26",
        "status": STATUS_COMPLETED
    },
    {
        "id": 9,
        "client_name": "Елизавета 'Корона' Царевна",
        "services": ["Королевское бритье опасной бритвой"],
        "master_id": 4,
        "date": "2025-03-27",
        "status": STATUS_NEW
    },
    {
        "id": 10,
        "client_name": "Добрыня 'Богатырь' Никитич",
        "services": ["Стрижка бороды 'Боярин'", "Плетение косичек 'Викинг'", "Массаж головы 'Озарение'"],
        "master_id": 5,
        "date": "2025-03-28",
        "status": STATUS_COMPLETED
    }
]