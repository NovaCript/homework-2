from flask import Flask, render_template, request

from database import db, Book, Genre

app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = "sqlite:///project.db"
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    fantasy = Genre(
        name='Фантастика',
        description='Это невозможно!'
    )

    book2 = Book(
        title='Код без ошибок',
        author='Самый умный',
        annotation='Я покажу как это делается...',
        genre=fantasy
    )
    detective = Genre(
        name='Детектив',
        description='Загадки будут раскрыты.'
    )

    book1 = Book(
        title='Flask',
        author='Человек Разумный',
        annotation='Главное практика, дружок...',
        genre=detective
    )
    db.session.add(detective)
    db.session.add(fantasy)
    db.session.add(book1)
    db.session.add(book2)

    db.session.commit()


@app.route('/view/')
def books():
    books = Book.query.order_by(Book.publication_date.desc()).limit(15).all()
    return render_template('viev_page_book.html', books=books)


@app.route('/genre/<int:genre_id>')
def books_by_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    return render_template(
        'books_by_genre.html',
        genre_name=genre.name,
        genre_description=genre.description,
        books=genre.books
    )


@app.route('/save', methods=['POST'])
def save():
    if request.method == 'POST':
        books_list = Book.query.all()
        for book in books_list:
            book_id = request.form.get('book_id_'+str(book.id))
            is_read = request.form.get('is_read_'+str(book.id))
            book_to_update = Book.query.get(book_id)
            if book_to_update:
                book_to_update.is_read = bool(is_read)
                db.session.commit()

        return 'Статусы книг обновлены успешно'
    return 'Неверный запрос'


if __name__ == '__main__':
    app.run(debug=True)
