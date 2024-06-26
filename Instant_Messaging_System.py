# -*- coding: utf-8 -*-
"""Untitled17.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1G8WprUwW5_u2IDI5VZU55Hwg68N-n7mS
"""

import sqlite3

#creating database and tables if they don't exist
def create_database():
    conn = sqlite3.connect('messaging.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY,
                 username TEXT,
                 password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY,
                 sender_id INTEGER,
                 receiver_id INTEGER,
                 message TEXT,
                 FOREIGN KEY(sender_id) REFERENCES users(id),
                 FOREIGN KEY(receiver_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

#Function to add a new user to system
def add_user(username, password):
    conn = sqlite3.connect('messaging.db')
    c = conn.cursor()
    c.execute('''INSERT INTO users (username, password)
                 VALUES (?, ?)''', (username, password))
    conn.commit()
    conn.close()

#Function to send message
def send_message(sender_id, receiver_id, message):
    conn = sqlite3.connect('messaging.db')
    c = conn.cursor()
    c.execute('''INSERT INTO messages (sender_id, receiver_id, message)
                 VALUES (?, ?, ?)''', (sender_id, receiver_id, message))
    conn.commit()
    conn.close()

#Function to view messages
def view_messages(user_id):
    conn = sqlite3.connect('messaging.db')
    c = conn.cursor()
    c.execute('''SELECT messages.message, users.username FROM messages
                 INNER JOIN users ON messages.sender_id = users.id
                 WHERE messages.receiver_id = ?''', (user_id,))
    messages = c.fetchall()
    conn.close()
    return messages

#Main function for user
def main():
    create_database()
    while True:
        print("\n*** Messaging System ***")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            add_user(username, password)
            print("User registered successfully!")

        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            conn = sqlite3.connect('messaging.db')
            c = conn.cursor()
            c.execute('''SELECT * FROM users WHERE username = ? AND password = ?''', (username, password))
            user = c.fetchone()
            conn.close()
            if user:
                user_id = user[0]
                print(f"Welcome, {username}!")
                while True:
                    print("\n1. Send Message")
                    print("2. View Messages")
                    print("3. Logout")

                    choice = input("Enter your choice: ")

                    if choice == '1':
                        receiver_username = input("Enter the username of the receiver: ")
                        message = input("Enter your message: ")
                        conn = sqlite3.connect('messaging.db')
                        c = conn.cursor()
                        c.execute('''SELECT * FROM users WHERE username = ?''', (receiver_username,))
                        receiver = c.fetchone()
                        conn.close()
                        if receiver:
                            receiver_id = receiver[0]
                            send_message(user_id, receiver_id, message)
                            print("Message sent successfully!")
                        else:
                            print("Receiver not found.")
                    elif choice == '2':
                        messages = view_messages(user_id)
                        if not messages:
                            print("No messages found.")
                        else:
                            print("\n*** Your Messages ***")
                            for msg in messages:
                                print(f"From: {msg[1]}, Message: {msg[0]}")
                    elif choice == '3':
                        print("Logged out successfully.")
                        break
                    else:
                        print("Invalid choice.")
            else:
                print("Invalid username or password.")

        elif choice == '3':
            print("Thank you for using the Messaging System.")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()