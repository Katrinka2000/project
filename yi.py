from flask import Flask, render_template, request
import requests
from flask_sqlalchemy import SQLAlchemy

url = "https://www.googleapis.com/books/v1/volumes" #это url google book apl
app = Flask(__name__)
def search_books(query):
    res = requests.get(url, params={'q': query, 'langRestrict': 'ru', 'maxResults': 15, 'key': 'AIzaSyCsGEFQ5iVLtTU9cydIlmm1LQYVCJ0LtKw'}).json()
    books = []
    for i in res.get('items', []): #все книги
        book = i['volumeInfo'] #информация о них
        image_links = book.get('imageLinks', {})
        # '' в скобочках означает то что будет выводиться если ничего не найдено
        books.append({'title': book.get('title', ''), 'authors': book.get('authors', ''),
                      'description': book.get('description', ''), 'thumbnail': image_links.get('thumbnail', ''),
                      'infoLink': book.get('infoLink', ''), 'publisher': book.get('publisher', ''),
                      'publishedDate': book.get('publishedDate', ''), 'pageCount': book.get('pageCount', ''),
                      'categories': book.get('categories', '')})
    return books

def search_author(author):
    res = requests.get(url, params={'q': author, 'langRestrict': 'ru', 'maxResults':15,
                                    'key': 'AIzaSyCsGEFQ5iVLtTU9cydIlmm1LQYVCJ0LtKw'}).json()
    books = []
    for i in res.get('items', []):
        book = i['volumeInfo']
        image_links = book.get('imageLinks', {})
        books.append({'title': book.get('title', ''), 'authors': book.get('authors', ''),
                      'description': book.get('description', ''), 'thumbnail': image_links.get('thumbnail', ''),
                      'infoLink': book.get('infoLink', ''), 'publisher': book.get('publisher', ''),
                      'publishedDate': book.get('publishedDate', ''), 'pageCount': book.get('pageCount', ''),
                      'categories': book.get('categories', '')})
    return books

@app.route("/")
def index():
    return render_template('index.html') # главная страничка

@app.route("/we")
def we():
    return render_template('we.html') # о нас

@app.route("/genre")
def genre():
    return render_template('genre.html') # различные жанры

@app.route("/main")
def main():
    return render_template('main.html') # профиль

@app.route("/top")
def top():
    return render_template('top.html') # страница с рейтингом книг

@app.route("/writer", methods=["GET", "POST"])
def writer():
    books = []
    if request.method == "POST":
        author = request.form.get("author")
        books = search_author(author)
    return render_template('writer.html', books=books) # писатели


@app.route("/book", methods=["GET", "POST"])
def book():
    books = []
    if request.method == "POST": #проверка отправил пользователь запрос или нет
        query = request.form.get("query")#запрос, который отправил пользователь
        if query:
            books = search_books(query)
    return render_template("book.html", books=books) # страница с книгами

if __name__ == '__main__':
    app.run(debug=True, port=3000, host="127.0.0.1")
