from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import author

class Book: 
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.on_author = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    ##Recupera info por cada instancia de libro creada
    @classmethod
    def get_books(cls):
        query= "SELECT * from books;"
        results = connectToMySQL('books_schema').query_db(query)
        books = []
        for book in results:
            books.append(cls(book))
        return books
    
    ##Crea instancia de libro en database 
    @classmethod
    def save_book(cls, data):
        query = "INSERT INTO books(title, num_of_pages, created_at, updated_at) VALUES (%(title)s, %(num_of_pages)s, NOW(), NOW());"
        new_book = connectToMySQL('books_schema').query_db(query, data)
        return new_book
    
    ##Relacion de many-to-many con autores
    @classmethod
    def books_with_authors(cls, data):
        query = "SELECT * FROM books LEFT JOIN favorites ON favorites.book_id = books.id LEFT JOIN authors ON favorites.author_id = authors.id WHERE books.id = %(id)s"
        results = connectToMySQL('books_schema').query_db(query, data)
        book = cls(results[0])
        for row  in results:
            author_data = {
                "id" : row["authors.id"],
                "name" : row["name"],
                "created_at": row["authors.created_at"],
                "updated_at": row["authors.updated_at"]
            }
            book.on_author.append(author.Author(author_data))
        return book
    
    ##BONUS NINJA: En el desplegable solo salen los NO favoritos aun
    @classmethod
    def rest_books(cls, data):
        query = "SELECT * FROM books WHERE books.id NOT IN (SELECT book_id FROM favorites WHERE author_id = %(id)s);"
        results = connectToMySQL('books_schema').query_db(query, data)
        books = []
        for row in results:
            books.append(cls(row))
        return books
    

