
import sqlite3

# Connect to the database
def connect_db():
    connection = sqlite3.connect("tyler.db")
    return connection


# Create database tables
def create_tables():

    connection = connect_db()
    cursor = connection.cursor()

    # Tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            deadline TEXT,
            priority TEXT,
            completed INTEGER DEFAULT 0
        )
    """)

    # Events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            event_date TEXT NOT NULL,
            start_time TEXT,
            end_time TEXT,
            category TEXT
        )
    """)

    # Goals table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT,
            description TEXT
        )
    """)
    
    # Transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            transaction_date TEXT NOT NULL,
            platform TEXT,
            description TEXT
        )
    """)
    

    connection.commit()
    connection.close()


# Add a new task
def add_task(title, deadline=None, priority="Medium"):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tasks (title, deadline, priority)
        VALUES (?, ?, ?)
    """, (title, deadline, priority))

    connection.commit()
    connection.close()


# Retrieve all tasks
def get_tasks():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    connection.close()

    return tasks


# Add a new event
def add_event(title, event_date, start_time, end_time, category):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO events
        (title, event_date, start_time, end_time, category)
        VALUES (?, ?, ?, ?, ?)
    """, (title, event_date, start_time, end_time, category))

    connection.commit()
    connection.close()


# Retrieve all events
def get_events():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM events")

    events = cursor.fetchall()

    connection.close()

    return events


# Add a new goal
def add_goal(title, category, description):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO goals (title, category, description)
        VALUES (?, ?, ?)
    """, (title, category, description))

    


    connection.commit()
    connection.close()


# Retrieve all goals
def get_goals():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM goals")

    goals = cursor.fetchall()

    connection.close()

    return goals

# Add a new transaction
def add_transaction(transaction_type, category, amount,
                    transaction_date, platform=None, description=None):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (transaction_type, category, amount, transaction_date, platform, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (transaction_type, category, amount, transaction_date, platform, description))

    connection.commit()
    connection.close()


# Retrieve all transactions
def get_transactions():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM transactions ORDER BY transaction_date DESC, id DESC")

    transactions = cursor.fetchall()

    connection.close()

    return transactions

# Update a task's completion status
def update_task_status(task_id, completed):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tasks
        SET completed = ?
        WHERE id = ?
    """, (int(completed), task_id))

    connection.commit()
    connection.close()

# Delete a transaction
def delete_transaction(transaction_id):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE id = ?",
         (transaction_id,)
        )

    connection.commit()
    connection.close()