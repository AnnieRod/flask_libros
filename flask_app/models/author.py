
from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import book

class Author: 
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.books = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

##Recupera info por cada instancia creada
    @classmethod
    def get_authors(cls):
        query= "SELECT * FROM authors;"
        authors = []
        results = connectToMySQL('books_schema').query_db(query)
        for author in results:
            authors.append(cls(author))
        return authors

## Crea instancia de author e integra registro en base de datos
    @classmethod
    def save_author(cls, data):
        query = "INSERT INTO authors(name, created_at, updated_at) VALUES (%(name)s, NOW(), NOW());"
        new_author = connectToMySQL('books_schema').query_db(query, data)
        return new_author

##Relacion de many-to-many con libros
    @classmethod
    def authors_with_books(cls, data):
        query = "SELECT * FROM authors LEFT JOIN favorites ON favorites.author_id = authors.id LEFT JOIN books ON favorites.book_id = books.id WHERE authors.id = %(id)s"
        results = connectToMySQL('books_schema').query_db(query, data)
        author = cls(results[0])
        for row in results:
            book_data = {
                "id" : row["books.id"],
                "title" : row["title"],
                "num_of_pages" : row["num_of_pages"],
                "created_at": row["books.created_at"],
                "updated_at": row["books.updated_at"]
            }
            author.books.append(book.Book(book_data))
        return author

##Añadir libros a favoritos
    @classmethod
    def add_book(cls, data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"
        return connectToMySQL('books_schema').query_db(query, data)

##BONUS NINJA: En el desplegable solo salen los autores que NO han marcado como favorito 
    @classmethod
    def rest_authors(cls, data):
        query = "SELECT * FROM authors WHERE authors.id NOT IN (SELECT author_id FROM favorites WHERE book_id = %(id)s);"
        results = connectToMySQL('books_schema').query_db(query, data)
        authors = []
        for row in results:
            authors.append(cls(row))
        return authors