# SimplexParsing
Парсинг сайта с решением систем уравнений.

Выполнила Гилязова Альбина.

Июль 2024.

# Технологии

Python, Selenium, BeautifulSoup.

# Как запустить проект

1. Установить браузер Firefox.
Программа тестировалась на Firefox 127.0.2.

2. Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/Knivy/SimplexParsing.git
```

```
cd SimplexParsing
```

3. Cоздать и активировать виртуальное окружение (должен быть установлен Python 3.12):

* Если у вас Linux/macOS

    ```
    python3 -m venv env
    source env/bin/activate
    ```

* Если у вас Windows

    ```
    python -m venv env
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

4. Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

5. Задать в parsing.py нужные вводные данные.

6. Запустить файл parsing.py, например, в командной строке Windows:

```
python parsing.py
```
