import sqlite3

def add_user(name, email):
    # Connect to the SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Insert user data into the users table
    cursor.execute('''
        INSERT INTO users (name, email)
        VALUES (?, ?)
    ''', (name, email))

    # Commit changes and close connection
    conn.commit()
    conn.close()

def view_users():
    # Connect to the SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Query all users from the users table
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()

    # Close connection
    conn.close()

    return rows

# Example usage:
if __name__ == "__main__":
    # Add a user
    add_user('John Doe', 'john.doe@example.com')

    # View all users
    users = view_users()
    for user in users:
        print(user)