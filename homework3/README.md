# TODO-List

## Description

Simple TODO list implemented with `Flask`

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

Вам необходимо реализовать веб-сервис для ведения ToDo списка. 

### Основная бизнес-логика: 
* Задача в списке — это только описание, т.е. нет заголовка, сроков и т.д. 
* Задача может быть либо сделана, либо нет. Если человек случайно создал задачу, то ему необходимо нажать “сделано”, чтобы эта задача исчезла. 
* По умолчанию должны отображаться только несделанные задачи. Однако необходима возможность просматривать: 
* * только сделанные задачи 
* * только несделанные задачи 
* * все задачи 


Концептуально список должен выглядеть примерно так:

![todo](https://user-images.githubusercontent.com/20886375/166250659-40e83cef-2c25-46a3-b865-899d41f59ab0.jpg)

### Усложненный вариант: 
* Реализовать пагинацию. По 10 задач на странице. Способ пагинации на ваше усмотрение. 
* Реализовать фильтрацию по подстроке — можно найти все задачи с данной подстрокой в описании. 

### Технические особенности: 
* Используем стандартный flask run для запуска
* Страницы должны формироваться на стороне сервера с помощью   jinja   . 
* Внешний вид страниц не оценивается — можно не делать никаких стилей css. 
* Для создания новых записей используем html-формы (POST запрос на отдельный эндпоинт с данными формы). 
* Для фильтраций (по статусу задачи, по подстроке) используем ссылки с GET параметрами, по которым получаем новую версию страницы с нужными данными. Например: 
* * GET /tasks 
* * GET /tasks?status=active 
* * GET /tasks?status=active&filter=string 
* * ... 
* Использование базы данных оцениваться не будет— все данные можно хранить где угодно (хоть в оперативной памяти). 
* Сохранять сессии и реализовывать аутентификацию не нужно. 

### Дополнительные требования: 
* Тесты. make test  должен запускать все тесты, т.к. эта команда используется в CI
* Уровень покрытия тестами - 90%
* Добавление и удаление элементов должно логироваться.
* Успешное прохождение линтеров. Проверить это можно с помощью make lint. Перед проверкой используйте make format, чтобы автоматически исправить некоторые недочеты. Можно сразу запускать make format lint , чтобы не делать несколько вызовов. 
* Запуск сервиса по команде make up. 
* Если используете БД, то используйте sqlite

Советуем попробовать отделить логику приложения от представления интерфейса взаимодействия. Это нужно в том числе для боле простого и качественного тестирования.
