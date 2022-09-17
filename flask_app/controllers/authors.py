from flask import request, redirect, render_template

from flask_app import app

from flask_app.models.author import Author

from flask_app.models.book import Book

app.secret_key = "somerandompassword"

##Dirige a pagina Home de librería
@app.route('/')
def start_app():
    return redirect ('/authors')

##Recupera info autores creados
@app.route('/authors')
def all_authors():
    return render_template ("authors.html", authors = Author.get_authors())

##  guardar info para crear el author segun info de form
@app.route('/authors/new', methods = ['POST'])
def create_author():
    Author.save_author(request.form)
    return redirect('/authors')

## author con libros favoritos
@app.route('/authors/<int:id>')
def fav_authors(id):
    data = {
        "id": id
        }
    return render_template ("fav_author.html", author = Author.authors_with_books(data), rest_books = Book.rest_books(data))

## Agrega libro favorito al autor 
@app.route("/bookfav", methods = ['POST'])
def add_favorite():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    Author.add_book(data)
    return redirect (f"/authors/{request.form['author_id']}")