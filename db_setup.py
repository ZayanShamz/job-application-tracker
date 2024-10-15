import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create login table
    cursor.execute('''CREATE TABLE IF NOT EXISTS login (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL)''')

    # Create jobs table
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        login_id INTEGER,
                        company_name TEXT NOT NULL,
                        job_title TEXT NOT NULL,
                        job_description TEXT,
                        job_requirements TEXT,
                        status TEXT,
                        follow_up TEXT, 
                        platform TEXT,
                        date TEXT,
                        FOREIGN KEY (login_id) REFERENCES login (id))''')


    conn.commit()
    conn.close()



if __name__ == '__main__':
    init_db()