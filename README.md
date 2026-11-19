# Course bot
Бот с интегрированной системой оплаты. Предназначен для продажи одного определенного товара, например пособия.
Если успешная оплата не может быть записана в БД, бот вызывает refund_star_payment и возвращает пользователю Stars.


# Сценарий использования 
/start → /buy → подтверждение или отмена
                         ├── отмена → конец сценария
                         └── подтверждение → invoice → оплата
                                                   → pre_checkout-проверка
                                                   → запись покупки
                                                   → /get


# Структура 

- course_bot:
    - heandlers:
        - buy.py
        - get_course.py
        - kb.py
        - pre_check.py
        - start.py
    - models:
        - agent.py
        - buy_class.py
        - db.py
        - payload.py
    - base.py
    - config.py
    - main.py
    - product.py
    - test_course.py
    - requirements.txt
    - README.md

# Запуск и тесты

Из папки проекта:

```bash

python -m venv venv
source venv/bin/activate # для windows source venv/Scripts/activate
pip install -r requirements.txt
export BOT_TOKEN="токен_бота"
python main.py

```

Тест:

```bash

python -m pytest -q test_course.py

```


# ограничения :
- поддерживается только один заранее заданный товар
- нет каталога и таблицы товаров
- причины конфликтов БД не разделяются отдельно
- повреждённый payload в get_paid не обрабатывается отдельной веткой
- тесты не проверяют реальный Telegram API и реальный возврат