from flask import request, redirect, render_template

from flask_app import app

from flask_app.models.author import Author

from flask_app.models.book import Book

## LIBROS: Recupera info de libros
@app.route('/books')
def all_books():
    return render_template ("books.html", books = Book.get_books())

##Recibe info de form para creación de instancia de libro
@app.route('/books/new', methods = ['POST'])
def create_book():
    Book.save_book(request.form)
    return redirect('/books')

##Libros con el autor que lo escogio como fav
@app.route('/books/<int:id>')
def fav_books(id):
    data = {
        "id": id
        }
    return render_template ("fav_book.html", book = Book.books_with_authors(data), rest_authors = Author.rest_authors(data))

## Agrega autor que escogio al libro como favorito
@app.route("/authorfav", methods = ['POST'])
def add_author():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    Author.add_book(data)
    return redirect (f"/books/{request.form['book_id']}")