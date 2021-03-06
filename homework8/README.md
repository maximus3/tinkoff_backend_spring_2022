# Programming contest

## Description:
Web-app for programming contests. Can check your solutions on Python.

## Задание:

Задача - написать сервис для создания контестов по программированию на Python.

### Бизнес-логика

- Пользователь может зарегистрироваться и войти в систему.
- Пользователь может зарегистрироваться для участия в контесте.
- Пользователь может отправлять неограниченное количество решений для каждой задачи.
- Пользователь должен видеть свои баллы за контест и каждое отдельное решение.
- Пользователь должен видеть статус отправленного решения (ожидание, тестирование, ОК, неправильный ответ, ошибка, превышено время выполнения).

### Технические особенности

- Сервис должен хранить все данные в БД.
- Сервис должен работать в докере.
- Решения должны проверяться в отдельном докер-контейнере.
- Должны приниматься решения на языке Python.
- Должно быть ограничение по времени в 1 секунду на каждое решение.
- Любые ошибки в пользовательских решениях не должны ломать работу сервиса.
- Обработка решений должна быть реализована через redis.

## Commands

### Docker  clean, build, up, clean
    make docker

### Up docker container:
    make docker-up

### Down docker container:
    make docker-down

### Create venv (if no docker):
    make venv

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

Курсовая работа условно состоит из двух частей:

### Подготовка задачи

Нужно придумать идею для небольшого проекта. Это может быть клон уже существующих онлайн сервисов или какой-то pet project на тему своего хобби. Например:

* клон twitter - платформа для микроблогов
* сервис для онлайн голосования
* сервис для онлайн викторин
* сервис с архивом записей аккордов различных песен для гитары
* онлайн игра, можно взять классические шахматы или “3Д-экшон с возможностью грабить караваны”

Далее вы должны написать задание, по типу тех, которые были в предыдущих домашних работах. Задание должно быть на разработку БЭКЕНД части сервиса (фронтенд не учитываем) с описанием сущностей, технологий, требований к задаче, пояснениями по выбору того или иного технологического стека, если посчитаете нужным. Это описание должно быть в README файле в репозитории с курсовой работой.

Веб фрэймворки, базы данных, очереди выбираются на ваше усмотрение, но рекомендуем взять то, с чем успели поработать в течение курса.

Мы будем оценивать понятность постановки задачи, ее сложность (тривиальные проекты получат меньше балов, но слишком сложные задачи не стоит ставить, иначе можно не справиться). Также не стоит без крайней уверенности ставить себе задачу на микросервисную систему, лучше остановиться на хорошо спроектированном монолите.

### Реализация

По написанному заданию нужно разработать бэкенд сервис с учетом требований, которые мы ранее предъявляли к домашним работам. А именно:

* Покрыть сервис тестами (make test).
* Покрыть код аннотациями типов (make lint запускает mypy для проверки).
* Код должен проходить проверки линтеров и быть автоматически отформатирован (make format lint).
* Сервис запускается по команде make up. 
* Все зависимости фиксируются через poetry. 
* Сервис запускается в докер контейнере. 

Максимальный бал, который можно получить за курсовую работу 20. Работа будет проверяться в том же порядке, что и прочие домашние задания. 

Крайний срок 10 мая. После него мы проставим оценки по тому, что будет готово и выложено на тот момент.