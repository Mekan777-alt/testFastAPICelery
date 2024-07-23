import random
import psycopg2
from faker import Faker
from core.config import settings

fake = Faker()

DATABASE_URL = f"dbname={settings.db_name} user={settings.db_user} password={settings.db_password} host={settings.db_host}"
connection = psycopg2.connect(DATABASE_URL)
cursor = connection.cursor()


def create_test_data(cursor, num_authors=10, num_books=50, num_genres=10):
    for _ in range(num_authors):
        first_name = fake.first_name()
        last_name = fake.last_name()
        avatar = fake.image_url()
        cursor.execute("""
            INSERT INTO authors (first_name, last_name, avatar)
            VALUES (%s, %s, %s)
        """, (first_name, last_name, avatar))
    connection.commit()

    cursor.execute("SELECT id FROM authors")
    authors = cursor.fetchall()

    for _ in range(num_genres):
        name = fake.word()
        cursor.execute("""
            INSERT INTO genres (name)
            VALUES (%s)
        """, (name,))
    connection.commit()

    cursor.execute("SELECT id FROM genres")
    genres = cursor.fetchall()

    for _ in range(num_books):
        author_id = random.choice(authors)[0]
        title = fake.text(max_nb_chars=20)
        price = round(fake.random_number(digits=2), 2)
        pages = fake.random_number(digits=3)
        cursor.execute("""
            INSERT INTO books (title, price, pages, author_id)
            VALUES (%s, %s, %s, %s)
        """, (title, price, pages, author_id))

        # Получение ID созданной книги
        cursor.execute("SELECT id FROM books ORDER BY id DESC LIMIT 1")
        book_id = cursor.fetchone()[0]

        # Ассоциация книги с жанрами
        num_associations = random.randint(1, 3)
        associations = set()
        for _ in range(num_associations):
            genre_id = random.choice(genres)[0]
            if (book_id, genre_id) not in associations:
                associations.add((book_id, genre_id))
                cursor.execute("""
                    INSERT INTO book_genre_association (book_id, genre_id)
                    VALUES (%s, %s)
                """, (book_id, genre_id))
    connection.commit()


create_test_data(cursor)

cursor.close()
connection.close()
