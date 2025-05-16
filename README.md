# weather-parser
# Парсер погоды с OpenWeatherMap
Скрипт, который получает прогноз погоды через API OpenWeatherMap, сохраняет данные в CSV и строит график температуры.

## Возможности
- Получает прогноз погоды на 5 дней для указанного города.
- Сохраняет данные в `weather.csv`.
- Создаёт график температуры в `weather_plot.png`.

## Технологии
- Python, requests, pandas, Matplotlib

## Установка
1. Клонируйте репозиторий: `git clone https://github.com/yourusername/weather-parser`
2. Создайте виртуальное окружение: `python -m venv venv`
3. Активируйте: `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
4. Установите зависимости: `pip install -r requirements.txt`
5. Укажите API-ключ в `weather.py`
6. Запустите: `python weather.py`

## Примечания
- Получите API-ключ на [OpenWeatherMap](https://openweathermap.org).
- Вывод включает `weather.csv` и `weather_plot.png`.
