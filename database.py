from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publication_date = db.Column(db.DateTime, nullable=False, default=func.now())
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    annotation = db.Column(db.Text, nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id', ondelete='SET NULL'))
    genre = relationship('Genre', back_populates='books')


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)

    books = relationship('Book', back_populates='genre')
