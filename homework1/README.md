# BattleShip

## Description

Цель игры - уничтожить все корабли противников.

Обозначения:
* 0 - корабль
* \* - попадание в корабль
* . - пустое место
* E - промах

Запуск игры происходит с параметрами height и width, где height — длина поля, width — ширина поля. Эти параметры по умолчанию равны 10.

Вы играете против компьютера, ходы происходят по очереди.

Нужно вводить ходы в формате БУКВАЧИСЛО или БУКВА ЧИСЛО, например: B1, C12, D 16.

Чтобы сохранить игру, введите save вместо хода.

Чтобы загрузить игру, введите yes или y в консоль при запуске программы (если сохранение существует).

Также в игре присутствуют ключ --automove для автоматического выбора ходов (нужно нажимать Enter после каждого хода) и ключ --autoplay для автоматической игры двух ботов (игра завершится автоматически).

## Commands

### Run app:
    python main.py

## Task Description:

### Описание 

Вам предстоит написать консольный вариант игры. Вы можете выбрать одну из двух задач. За выполнение стандартной задачи вы можете получить максимум 8 баллов, а за задачу повышенной сложности — 10. 

Механику взаимодействия с игрой вы можете придумать сами, однако после каждого хода на экране должно присутствовать актуальное изображение игрового поля. 

Вы можете посмотреть на игру "slapjack", чтобы понять технические особенности работы с консолью применительно к играм. Данная реализация является примером кода неплохого качества, однако не стоит ориентироваться на нее как на идеальный вариант. Мы призываем вас использовать хорошие практики разработки. Помните, ваш код будут читать люди — постарайтесь написать максимально читаемый и логичный код. 

### Требования (обязательно к реализации!)
* Параметры игры должны приниматься с помощью аргументов командной строки. Для этого нужно воспользоваться библиотекой https://github.com/tiangolo/typer
* Должно быть описание проекта (README.md) — как минимум, с описанием того, как играть в игру.
* Должна быть реализована возможность сохранить игру, чтобы после перезапуска скрипта продолжить с того же места. Для реализации может быть удобно воспользоваться модулем pickle.
* Игра должна играть против вас, алгоритм выбора хода не важен, даже если противник делает случайные ходы (но допустимые с точки зрения правил).
* Код должен быть отформатирован с помощью https://github.com/psf/black
P.S. если вы используете Windows и curses , у вас могут быть проблемы. Решение этой проблемы находится здесь https://stackoverflow.com/questions/32417379/what-is-needed-for-curses-in-python-3-4-on-windows7. 

### Стандартная задача 

Ваша задача — реализовать консольный вариант игры "Крестики-нолики". 

В игре должна присутствовать возможность выбирать произвольный размер поля N K, где N — длина поля, K — ширина поля. 

Условие победы — min (N,K) последовательных крестиков / ноликов по горизонтали, по вертикали или по диагонали. 

На вход как аргументы командой строки программа должна принимать параметры N и K. 

### Задача повышенной сложности 

Ваша задача — реализовать консольный вариант игры "Морской бой". 

В игре должна присутствовать возможность выбирать произвольный размер поля N K, где N — длина поля, K — ширина поля.

Должна быть возможность расстановки кораблей автоматически без участия игрока.

Количество и возможные размеры кораблей должны вычисляться автоматически, исходя из пропорций в оригинальной версии игры. Вы можете не рассматривать размер карты меньше, чем 5x5. 

На вход как аргументы командой строки программа должна принимать параметры N и K. 
