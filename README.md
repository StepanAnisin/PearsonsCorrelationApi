# PearsonsCorrelationApi

# Описание задачи: #
Есть пользователи, от которых получены некоторые данные о 2-ух показателях здоровья (например, пульс, давление) за определённые даты.


Необходимо реализовать HTTP web-сервис для сопоставления данных двух векторов по датам и последующего рассчёта корреляции Пирсона между ними. Полученные результаты необходимо сохранить в базу данных и реализовать конечную точку для их чтения.

Данные могут быть повреждены, т.е. могут иметь тип, не соответствующий формату входных данных; по датам двух векторов может не оказаться соответствий, и т.д.
# Quick start #

Скопируйте репозиторий в указанную вами директорию и выполните из ней команды:

` docker-compose build `

` docker-compose up -d `

# Docker контейнеры #
Для каждого элемента данного проекта реализован отдельный контейнер.

* app: где запущено Flask web-приложение
* redis: redis сервер
* worker: достаёт из очереди задачу и выполняет её. Здесь реализована бизнес-логика
* db: база данных PostgreSQL

# Реализация задачи #

По ходу выполнения, были реализованы 4 конечные точки:

* **/calculate**

Ставит в очередь задачу по вычислению и сохранению в БД результата вычисления метрики. Возвращает id задачи

Формат входных данных:
```
{
        "user_id": int,
        "data": {
            "x_data_type": str,
            "y_data_type": str,
            "x": [
                {
                    "date": YYYY-MM-DD,
                    "value": float,
                },
                ...
            ],
            "y": [
                {
                    "date": YYYY-MM-DD,
                    "value": float,
                },
                ...
            ]
        }
    }
```

* **/correlation?x_data_type=str&y_data_type=str&user_id=int**

Ставит в очередь задачу на чтению данных в БД по входным параметрам в запросе. Возвращает id задачи.


* **/task-status/<task_id>**

Возвращает статус выполнения задачи


* **/task-result/<task_id>**

Возвращает результат выполнения задачи





**Все функции, отвечающие за бизнес-логику покрыты юнит-тестами и в проекте доступны в директории ` ../src/tests `**

# Postman коллекция для тестирования: # 
https://www.getpostman.com/collections/fdcd782198f4623a7112