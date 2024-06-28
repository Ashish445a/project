import requests
from bs4 import BeautifulSoup
import sqlite3


conn = sqlite3.connect('books.db')
c = conn.cursor()
c.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price TEXT NOT NULL
        )
    ''')
   


url = 'https://books.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
book_containers = soup.find_all('article', class_='product_pod')

books = []
for container in book_containers:
    title = container.h3.a.text
    price = container.find('div', class_='product_price').p.text
    books.append((title, price))


def insert_books(books):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.executemany('INSERT INTO books (title, price) VALUES (?, ?)', books)
    conn.commit()
    conn.close()

insert_books(books)

