# Image Resizer

## Description

REST-API square image resizer implemented with FastAPI.

You can resize your square images to 32x32 or 64x64.

To create task - POST on `/tasks` with image encoded in base64 format in `data` field.

To check status - GET on `/tasks/{id}`.

To get image - GET on `/tasks/{id}/image?size=<original, 32 или 64>`.

## Commands

### Docker clean, build, up, clean
    make docker

### Up docker container:
    make docker-up

### Down docker container:
    make docker-down

### Create venv (if no docker):
    make venv

### Run app (without workers, only web):
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
Ваша задача реализовать веб-сервер, который предоставляет API для изменения размера картинок. 

### Бизнес-логика 
При POST-запросе на адрес “/tasks” в теле запроса передается картинка. В ответ приходит id задачи, статус выполнения задачи, используя который можно будет получить измененную картинку. HTTP-код ответа должен равняться 201.

Далее пользователь может проверять статус выполнения задачи с помощью GET-запроса на адрес “/tasks/<id задачи>”. В ответ приходит id задачи, статус выполнения задачи (WAITING, IN_PROGRESS, DONE, FAILED). HTTP-код ответа — 200. 

Когда задача окажется выполненной, пользователь может получить картинку в нужном размере с помощью GET-запроса на адрес “/tasks/<id задачи>/image?size=<64, 32 или original>”. В ответ пользователь должен получить код ответа 200 и: 

* картинку соответствующего размера 

С точки зрения сервера процесс организован так: 

* Сервер после получения картинки сохраняет ее в redis и помещает задачу в очередь задач. 
* Воркеры (обособленные python-процессы) берут задачу из очереди, пережимают картинку во все необходимые размеры и сохраняют их как отдельные объекты в redis. 


### Технические особенности 
* На вход и на выход в теле запроса должен быть json. 
* Данные храним в redis 
* Для асинхронной обработки задач в простом варианте используем https://python-rq.org/ 
* Используйте redis в режиме “in-memory”. Нужно запустить отдельным контейнером в docker’е. 
* Для работы с картинками рекомендуем использовать библиотеки Pillow и  base64  . 
* Пережимать картинку нужно только в размеры 64x64 и 32x32. 
* На вход принимаются только квадратные картинки. 
* Пережатые картинки сохранять в redis закодированными в base64 
* Задача не предполагает графического интерфейса (html, etc.) 
* Аутентификация не нужна. 
* Пагинация не нужна. 

### Обязательные требования 
* Покрыть сервис тестами (make test) 
* Покрыть код аннотациями типов. (make lint запускает mypy для проверки) 
* Код должен проходить проверки линтеров и быть автоматически отформатирован (make format lint) 
* Сервис запускается по команде make up. 
* Все зависимости фиксируются через poetry. 
* sqlalchemy не требуется. 
* Сервис и воркеры должны запускаться в отдельных docker-контейнерах. 


### Усложненный вариант 
Реализовать свой механизм очередей задач на основе redis. Очереди должны быть устойчивы к отказам. Это означает, что не должно возникнуть ситуации, когда задача берется на обработку из очереди, но при сбое обработчика — теряется. Описание возможной реализации:   https://redis.io/commands/rpoplpush   

Можете считать, что redis сохраняет данные надежно, т.е. внутри него данные никогда не исчезают. 
