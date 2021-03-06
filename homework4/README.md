# CryptoStock Market

## Description

REST-API service for cryptotrading.

## Commands

### Run app:
    make up

### Run tests:
    make test

### Run linters:
    make lint

### Run formatters:
    make format

### Run format and lint code then run tests:
    make check

## Task Description:

### Описание

Ваша задача написать сервис биржу криптовалют.

За выполнение стандартной задачи вы можете получить максимум 8 баллов, а за задачу повышенной сложности — 10. 

Пользователь должен иметь возможность зарегистрироваться на бирже. 

После регистрации ему выдается 1000 у.е. У пользователя должна быть возможность узнать текущую сумму у.е. на счете. 

Также пользователь может узнать свой портфель криптовалют (т.е. сколько каждой валюты у него сейчас есть). Изначально на бирже есть 5 криптовалют (названия придумайте сами), но можно добавлять новые. 

Каждую валюту можно купить или продать за у.е, соответственно у пользователя должна быть возможность посмотреть курс покупки / продажи для каждой валюты, а также просмотреть все совершенные операции покупок / продаж. 

Общее количество единиц криптовалюты или у.е. в системе не ограничено. 

Пользователь может купить или продать сколько угодно единиц валюты по своему желанию, однако количество у.е на счете всегда должно оставаться неотрицательным. Если пользователь хочет совершить операцию, на которую ему не хватает у.е. — биржа должна отказать. 

* Сервис нужно предоставлять в виде html, который генерируется на стороне сервера (jinja2), или через json api (формат можно выбрать на свое усмотрение). Выбирайте один из предложенных вариантов.
* Нужно спроектировать нормализованную схему базы данных с разумными ограничениями (constraints).
* Нельзя хранить единицы валют в полях бд или в значениях в памяти с типом float. 
* Курсы валют должны каждые 10 секунд случайным образом увеличиваться или уменьшаться на 1-10%. Можно запустить отдельный поток / процесс внутри приложения для реализации этого поведения. 
* Пользователь не должен иметь возможности купить валюту по устаревшему значению курса, т.е. в операции покупки на сервер должна явно приходить стоимость, по которой клиент хотел купить валюту или время, когда была получены стоимость валюту. Сервер должен сверить, что курс все еще не изменился, прежде чем выполнять операцию, иначе возвращать ошибку. Это нужно, чтобы защитить пользователя от непредвиденных расходов.
* Аутентификация не нужна. При регистрации пользователя или осуществлении операций от его имени нужен только login.
* Пагинация нужна для списка совершенных операций. 

### Усложненный вариант

Реализовать дополнительно бота в виде отдельного python скрипта, который создает нового пользователя и затем, совершая операции от его имени, максимизирует прибыль у.е. от операций на бирже. Бот должен торговать некоторое заданное через параметры скрипта время, а потом отчитываться, сколько прибыли в у.е. он по итогу заработал.

### Требования (обязательно к реализации!)

* Покрыть сервис тестами (make test) 
* Покрыть код аннотациями типов. (make lint запускает mypy для проверки) 
* Код должен проходить проверки линтеров и быть автоматически отформатирован (make format lint) 
* Сервис запускается по команде make up. 
* Должно быть описание проекта (README.md) — с описанием того, как пользоваться сервисом.
* Все зависимости фиксируются через poetry. 
* БД должна быть обязательно — используйте sqlite. 
* Для работы с базой обязательно использовать sqlalchemy.

Использовать нужно именно sqlalchemy, а не обертки такие как flask-sqlalchemy, т.к. sqlalchemy позволяет работать в разных проектах с разным стеком технологий одинаковым образом. Именно эта универсальность и помогает разработчикам.
