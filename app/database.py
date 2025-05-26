import sqlite3

def init_db():
    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS searches (city TEXT PRIMARY KEY, count INTEGER DEFAULT 0)")
    conn.commit()
    conn.close()

def save_search(city: str):
    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    c.execute("INSERT INTO searches (city, count) VALUES (?, 1) ON CONFLICT(city) DO UPDATE SET count = count + 1", (city,))
    conn.commit()
    conn.close()

def get_search_stats():
    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    c.execute("SELECT city, count FROM searches ORDER BY count DESC")
    result = c.fetchall()
    conn.close()
    return {city: count for city, count in result}