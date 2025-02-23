# Для читающих
# Это проект Api сервера для расписания колледжа, который позволяет получать информацию о расписании по API используя Telegram бота или свои приложения.
# Pull реквесты будут активно рассматриваться и применяться в качестве обновлений, поэтому если хотите дополнить какой-либо функционал, будет очень круто.

# Инструкция по запуску Api сервера локально:
- Клонируете репозиторий к себе на компьютер
- Устанавливаете библиотеки указанные в requirements.txt
```
pip install -r requirements.txt
```
- Запускаете сервер используя main.py
```
python main.py
```
- Учитывайте, что для полноценной работы Api сервера, необходимо запустить парсер расписаний, сделать это можно через графический интерфейс по ссылке http://localhost:8000/admin/ChangesPage нажав на кнопку "Проверить Excel" или раскомментив
```python
Download()
AddToDatabase(ParsTwoTable())
```
(В таком случае парсер расписаний будет всегда запускаться при запуске Api сервера)
- Так же учитывайте, что парсер автоматически запускается каждые 24 часа работы сервера чтобы подгрузить новую информацию в БД.
## Работа Api сервера проверялась на python 3.12.8

# Документация для API расписания


## Получение списка всех групп

[{{ data.link }}/api/groups]

Возвращает список групп массивом в формате JSON.

**Пример:**

```json
[
    "АТ 21-11-1",
    "АТ 21-11-2",
    "АТ 21-11-3",
    ...
]
```

# Получение списка всех преподавателей
[{{ data.link }}/api/teachers]

Возвращает список преподавателей словарем, где ключ = id преподавателя.

**Пример:**

``` json
{
    "1": {
        "id": 1,
        "FirstName": "В.",
        "SecondName": "А.",
        "Surname": "Ткачук"
    },
    "2": {
        "id": 2,
        "FirstName": "В.",
        "SecondName": "С.",
        "Surname": "Белан"
    },
    "3": {
        "id": 3,
        "FirstName": "И.",
        "SecondName": "В.",
        "Surname": "Русских"
    },
    ...
}
```

# Получение списка всех возможных предметов

[{{ data.link }}/api/subjects]

Возвращает список предметов массивом в формате JSON.

Пример:

``` json
[
    "Иностранный язык",
    "Программирование",
    ...
]
```
# Получение списка всех кабинетов

[{{ data.link }}/api/classrooms]

Возвращает список кабинетов массивом в формате JSON, включая актовый и спортзал.

Пример:

``` json
[
    "101",
    "102",
    "103",
    ...
]
```

# Получение списка изменений по дате

[{{ data.link }}/api/changes_day?date={{ data.today }}]

Дата должна быть в формате (%Y-%m-%d).

Возвращает JSON словарь изменений для всех групп по дате, где ключ = id изменения.

Пример:

``` json
{
    "1": {
        "id": 1,
        "IsChange": true,
        "Date": "2023-09-18",
        "Group": "ИСиП 21-11-3",
        "Urok": 6,
        "Classroom": "891",
        "Prepod": "Ткачук В. А.",
        "Subject": "Разговоры о важном",
        "Comment": "Будет",
        "Delete": null
    },
    "2": {
        "id": 2,
        "IsChange": true,
        "Date": "2023-09-18",
        "Group": "ИСиП 21-11-3",
        "Urok": 6,
        "Classroom": "891",
        "Prepod": "Ткачук В. А.",
        "Subject": "Иностранный язык",
        "Comment": "Будет",
        "Delete": null
    },
    "3": {
        "id": 3,
        "IsChange": true,
        "Date": "2023-09-18",
        "Group": "ИСиП 21-11-3",
        "Urok": 6,
        "Classroom": "891",
        "Prepod": "Ткачук В. А.",
        "Subject": "Программирование",
        "Comment": "Будет",
        "Delete": 1
    },
    ...
}
```
# Получение расписания сразу с изменениями на день

[{{ data.link }}/api/class_day?date={{ data.today }}&group=ИСиП 21-11-3]

Возвращает список уроков на определенную дату и группу.

Пример:
```json
{
    "5": {
        "Subject": "Иностранный язык",
        "Prepod": "Ткачук В. А.",
        "Group": "ИСиП 21-11-3",
        "Date": "2023-09-18",
        "Number": 5,
        "Classroom": "891",
        "IsChange": false
    },
    "6": {
        "Date": "2023-09-18",
        "Group": "ИСиП 21-11-3",
        "Number": 6,
        "Classroom": "891",
        "Prepod": "Ткачук В. А.",
        "Subject": "Программирование",
        "Comment": "Будет",
        "Delete": null,
        "IsChange": true
    }
}
```

# Получение расписания сразу с изменениями на неделю

[{{ data.link }}/api/class_week?date={{ data.today }}&group=ИСиП 21-11-3]

Возвращает JSON массивы в словарях, ключи которых = id уроков, все это в большом словаре, в котором ключи = даты.

Пример:
```json
{
    "2023-09-18": {
        "5": {
            "Subject": "Программирование",
            "Prepod": "Ткачук В. А.",
            "Group": "ИСиП 21-11-3",
            "Date": "2023-09-18",
            "Number": 5,
            "Classroom": "101",
            "IsChange": false
        },
        "6": {
            "Date": "2023-09-18",
            "Group": "ИСиП 21-11-3",
            "Number": 6,
            "Classroom": "102",
            "Prepod": "Ткачук В. А.",
            "Subject": "Иностранный язык",
            "Comment": "Будет",
            "Delete": null,
            "IsChange": true
        }
    },
    "2023-09-19": {
        "7": {
            "Subject": "Разговоры о важном",
```
