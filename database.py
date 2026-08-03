import sqlite3
import os
print(os.getcwd())


def connect():

    connection = sqlite3.connect('contacts.db')
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts ( 
                   id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL,
                   last_name TEXT, phone TEXT NOT NULL)''')

    connection.commit()
    connection.close()


def add_contact(first_name, last_name, phone):
    connection = sqlite3.connect('contacts.db')
    cursor = connection.cursor()

    cursor.execute('''INSERT INTO contacts(first_name, last_name, phone)
                   VALUES (?, ?, ?)''', (first_name, last_name, phone))
    connection.commit()
    connection.close()


def get_contacts():
    connection = sqlite3.connect('contacts.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM contacts')

    contacts = cursor.fetchall()
    connection.close()
    return contacts


def delete_contact(contact_id):
    connection = sqlite3.connect('contacts.db')
    cursor = connection.cursor()

    cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))

    connection.commit()
    connection.close()


def update_contact(contact_id, first_name, last_name, phone):
    connection = sqlite3.connect('contacts.db')
    cursor = connection.cursor()

    cursor.execute('''UPDATE contacts SET first_name = ?, last_name = ?,
                    phone = ? WHERE id = ?''', (first_name, last_name, phone, contact_id))

    connection.commit()
    connection.close()


def get_contact(contact_id):

    connection = sqlite3.connect("contacts.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT first_name, last_name, phone FROM contacts WHERE id=?",
        (contact_id,)
    )

    contact = cursor.fetchone()

    connection.close()

    return contact


def delete_contact(contact_id):

    connection = sqlite3.connect("contacts.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM contacts WHERE id=?",
        (contact_id,)
    )

    connection.commit()
    connection.close()


def search_contacts(text):

    connection = sqlite3.connect("contacts.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM contacts
        WHERE first_name LIKE ?
        OR last_name LIKE ?
        OR phone LIKE ?
        """,
        (f"%{text}%", f"%{text}%", f"%{text}%")
    )

    contacts = cursor.fetchall()

    connection.close()

    return contacts
