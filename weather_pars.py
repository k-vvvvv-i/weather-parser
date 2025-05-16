import requests
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Настройки
API_KEY = "e90c319d2e267a32d287e9a8a50d3eda"  # Вставь свой API-ключ
CITIES = ["Moscow", "London", "Tokyo"]
DB_NAME = "weather.db"

def check_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather")
    print(cursor.fetchall())
    conn.close()
    
def init_db():
    """Инициализация базы данных SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS weather (city TEXT, temp REAL, date TEXT)")
    conn.commit()
    conn.close()
    logging.info("База данных инициализирована")

def fetch_weather(city):
    """Получение температуры через OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data["cod"] == 200:
            temp = data["main"]["temp"]
            logging.info(f"{city}: {temp}°C")
            return temp
        else:
            logging.error(f"Ошибка API для {city}: {data['message']}")
            return None
    except requests.RequestException as e:
        logging.error(f"Ошибка запроса для {city}: {e}")
        return None

def save_weather(city, temp):
    """Сохранение данных в SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("INSERT INTO weather (city, temp, date) VALUES (?, ?, ?)", (city, temp, date))
    conn.commit()
    conn.close()
    logging.info(f"Данные сохранены для {city}")

import matplotlib.pyplot as plt
from datetime import datetime

def plot_weather():
    """Построение графика температуры."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT city, temp, date FROM weather ORDER BY date")
    data = cursor.fetchall()
    conn.close()
    
    if not data:
        logging.warning("Нет данных для построения графика")
        return
    
    cities = list(set(d[0] for d in data))
    plt.figure(figsize=(10, 6))
    for city in cities:
        temps = [d[1] for d in data if d[0] == city]
        # Преобразуем строки дат в объекты datetime
        dates = [datetime.strptime(d[2], "%Y-%m-%d %H:%M") for d in data if d[0] == city]
        plt.plot(dates, temps, marker="o", label=city)
    
    plt.xlabel("Дата и время")
    plt.ylabel("Температура (°C)")
    plt.title("Температура в городах")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("weather_plot.png")
    plt.close()
    logging.info("График сохранен в weather_plot.png")

def main():
    init_db()
    for city in CITIES:
        temp = fetch_weather(city)
        if temp is not None:
            save_weather(city, temp)
    plot_weather()

if __name__ == "__main__":
    main()