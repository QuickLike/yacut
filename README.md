# [Проект yacut.](https://github.com/QuickLike/yacut)

## Технологии:

- Python
- Flask

## Описание проекта:

YaCut - Укоротитель ссылок.

### Запуск проекта:
Клонируйте [репозиторий](https://github.com/QuickLike/yacut) и перейдите в него в командной строке:
```
git clone https://github.com/QuickLike/yacut

cd yacut
```
Создайте виртуальное окружение и активируйте его
Windows
```
python -m venv venv
venv/Scripts/activate
```

Linux/Ubuntu/MacOS
```
python3 -m venv venv
source venv/bin/activate
```
Обновите pip:
```
python -m pip install --upgrade pip
```
Установите зависимости:
```
pip install -r requirements.txt
```
В корне проекта создайте файл .env, и добавьте туда переменные окружения
```
FLASK_APP=yacut
FLASK_DEBUG=<1_или_0>
DATABASE_URI=<тип_бд>:///<имя_бд>
SECRET_KEY=<любой_ключ>
```
Запуск сервера
```
flask run
```



## Автор

[Власов Эдуард](https://github.com/QuickLike)
