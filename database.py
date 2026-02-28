"""
SQLite Database for Portfolio
"""
import sqlite3

DB_NAME = "portfolio.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Visitors
    cursor.execute('''CREATE TABLE IF NOT EXISTS visitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT, user_agent TEXT, visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Skills
    cursor.execute('''CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, category TEXT, level INTEGER)''')
    
    # Projects
    cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, description TEXT, github_url TEXT, image_url TEXT)''')
    
    # Messages
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, email TEXT, message TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Seed Skills
    cursor.execute("SELECT COUNT(*) FROM skills")
    if cursor.fetchone()[0] == 0:
        skills = [("Python", "Language", 90), ("C", "Language", 85), ("C++", "Language", 80),
                  ("C#", "Language", 75), ("Mobile App Dev", "Framework", 85),
                  ("OOP", "Concept", 90), ("Advanced DB", "Database", 80), ("DIP", "Specialization", 75)]
        cursor.executemany("INSERT INTO skills (name, category, level) VALUES (?,?,?)", skills)
    
    # Seed Projects
    cursor.execute("SELECT COUNT(*) FROM projects")
    if cursor.fetchone()[0] == 0:
        projects = [("Daily Dua & Azkar App", "Mobile app for daily prayers and remembrances",
                    "https://github.com/Rubina-Bibi/Rubina-Bibi-RollN0-100069-TermProject-MobileApplicationDevelopmentProject-DailyDua-AzkarApp-",
                    "/static/images/project1.jpg"),
                   ("Document Scanner", "Digital image processing for document digitization",
                    "https://github.com/Rubina-Bibi/DIP-Project-Document-Scanner-100069-5th-Semester",
                    "/static/images/project2.jpg")]
        cursor.executemany("INSERT INTO projects (name, description, github_url, image_url) VALUES (?,?,?,?)", projects)
    
    conn.commit()
    conn.close()
    print("✅ Database ready!")

def get_skills():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, category, level FROM skills ORDER BY level DESC")
    data = cursor.fetchall()
    conn.close()
    return data

def get_projects():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, description, github_url, image_url FROM projects")
    data = cursor.fetchall()
    conn.close()
    return data

def add_visitor(ip, ua):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO visitors (ip, user_agent) VALUES (?, ?)", (ip, ua))
    conn.commit()
    conn.close()

def save_message(name, email, msg):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)", (name, email, msg))
    conn.commit()
    conn.close()