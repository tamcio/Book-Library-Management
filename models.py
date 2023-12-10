from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String)
    year = Column(Integer)
    loans = relationship('Loan', back_populates='book')

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError('Nie mozesz dodac ksiazki bez tytulu')
        return title


class Friend(Base):
    __tablename__ = 'friends'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, nullable=False)
    loans = relationship("Loan", back_populates="friend")

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError('Nieprawidlowy adres e-mail. Musi zawierac @')
        return email

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    friend_id = Column(Integer, ForeignKey('friends.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    loan_date = Column(DateTime, default=datetime.now)

    friend = relationship("Friend", back_populates="loans")
    book = relationship("Book", back_populates="loans")