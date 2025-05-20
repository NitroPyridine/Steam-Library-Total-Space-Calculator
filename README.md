# Steam Library Total Space Calculator

A script for calculating the required disk space to install your entire Steam library

1. Install Python 3.10+
You can download it from the [official website](https://www.python.org/downloads/);
2. Run `Run Steam Library Space Calculator.bat` or
Manually install dependencies with `pip install -r requirements.txt` and run `main.py`;
3. Enter your Steam API key [get it here](https://steamcommunity.com/dev/apikey);
4. Enter your SteamID [get it here](https://steamdb.info/calculator);

## How It Works

Using the Steam Web API, the program fetches your full game library — even if your profile is private.
For each game, the program visits its Steam Store page and searches for storage requirements.

---

Скрипт для подсчёта необходимого места на диске, для установки всей вашей библиотеки Steam

1. Установите Python 3.10+
Скачать можно с [официального сайта](https://www.python.org/downloads/);
2. Запустить `Run Steam Library Space Calculator.bat` или
Установите зависимости ручками `pip install -r requirements.txt` и запустите `main.py`;
3. Введите свой Steam API ключ [получить тут](https://steamcommunity.com/dev/apikey);
4. Введите ваш SteamID [получить тут](https://steamdb.info/calculator);

## Как это работает
С помощью Steam Web API программа получает список всех игр, которые принадлежат аккаунту, даже если профиль скрыт от публичного просмотра.
Для каждой игры программа переходит на страницу магазина Steam и ищет там информацию о минимальном или рекомендуемом размере на диске.
