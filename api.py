from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models import Book, Friend, Loan


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteka.db'
    db = SQLAlchemy(app)
    return app

def create_db():
    engine = create_engine('sqlite:///biblioteka.db')
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
    session = Session()
    return engine, Base, session

app = create_app()
engine, Base, session = create_db()

@app.route('/books', methods=['GET'])
def get_books():
    tab = []
    books = session.query(Book).all()
    for book in books:
        tab.append([book.id,book.title,book.author,book.year])
    return jsonify(tab)

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = session.query(Book).get(id)
    if book is None:
        return jsonify(error="Nie ma ksiazki z takim ID")
    return jsonify(f'ID: {book.id} | {book.title} napisana przez {book.author} wydana w roku {book.year}')

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    book = Book(title=data['title'], author=data['author'], year=data['year'])
    session.add(book)
    session.commit()
    return 'Ksiazka zostala dodana pomyslnie'

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book_data = request.get_json()
    book = session.query(Book).filter_by(id=id).first()
    if book is None:
        return jsonify({'error': 'Nie ma ksiazki z takim ID'})
    else:
        book.title = book_data['title']
        book.author = book_data['author']
        book.year = book_data['year']
        return "Ksiazka zostala zaktualizowana"


@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = session.query(Book).filter(Book.id == id).first()
    if book is None:
        return jsonify({'error': 'Nie ma ksiazki z takim ID'})
    else:
        session.delete(book)
        session.commit()
        return jsonify({'status': 'Usunieto Ksiazke'})


@app.route('/friends', methods=['GET'])
def get_friends():
    tab = []
    friends = session.query(Friend).all()
    for friend in friends:
        tab.append(f'ID: {friend.id} | Nazwa: {friend.name} | E-mail: {friend.email}')
    return jsonify(tab)


@app.route('/friends/<int:id>', methods=['GET'])
def get_friend(id):
    friend = session.query(Friend).get(id)
    if friend is None:
        return jsonify({'error': 'Nie masz kolegi z takim ID'})
    else:
        return jsonify(f'ID: {friend.id} | Nazwa: {friend.name} | E-mail: {friend.email}')

@app.route('/friends', methods=['POST'])
def create_friend():
    data = request.get_json()
    friend = Friend(name=data['name'], email=data['email'])
    session.add(friend)
    session.commit()
    return 'Kolega/Kolezanka zostal/a dodany/a pomyslnie'

@app.route('/friends/<int:id>', methods=['PUT'])
def update_friend(id):
    data = request.get_json()
    friend = session.query(Friend).get(id)
    if friend is None:
        return jsonify({'error': 'Nie masz kolegi z takim ID'})
    else:
        friend.name = data['name']
        friend.email = data['email']
        session.commit()
        return jsonify({'message': 'Zaktualizowano dane kolegi'})


@app.route('/friends/<int:id>', methods=['DELETE'])
def delete_friend(id):
    friend = session.query(Friend).filter_by(id=id).first()
    if friend is None:
        return jsonify({'status': 'Nie znaleziono kolegi'})
    else:
        session.delete(friend)
        session.commit()
        return jsonify({'status': 'Usunieto kolege'})

@app.route('/loan', methods=['GET'])
def get_loans():
    tab = []
    loans = session.query(Loan).all()
    for loan in loans:
        book = session.query(Book).get(loan.book_id)
        friend = session.query(Friend).get(loan.book_id)
        tab.append(f'ID: {loan.id} | Kolega o imieniu {friend.name} i ID: {loan.friend_id}, pozyczyl ksiazke: {book.title} o ID: {book.id} | dnia: {loan.loan_date}')
    return jsonify(tab)


@app.route('/loan/<int:id>', methods=['GET'])
def get_loan(id):
    loan = session.query(Loan).get(id)
    if loan:
        book = session.query(Book).get(loan.book_id)
        friend = session.query(Friend).get(loan.book_id)
        return jsonify(f'ID: {loan.id} | Kolega o imieniu {friend.name} i ID: {loan.friend_id}, pozyczyl ksiazke: {book.title} o ID: {book.id} | dnia: {loan.loan_date}')
    else:
        return jsonify({"error": f" Nie znaleziono pozyczki o ID {id}"})

@app.route('/loan', methods=['POST'])
def add_loan():
    json_data = request.get_json()
    loan = Loan(friend_id=json_data['friend_id'],book_id=json_data['book_id'])
    session.add(loan)
    session.commit()
    return jsonify({'status': 'Pomyślnie dodano wypożyczenie'})

@app.route('/loan/<int:loan_id>', methods=['PUT'])
def update_loan(loan_id):
    json_data = request.get_json()
    loan = session.query(Loan).filter_by(id=loan_id).one()
    if loan is None:
        return jsonify({'error': 'Nie ma pożyczki o takim ID'})
    else:
        loan.book_id = json_data['book_id']
        loan.friend_id = json_data['friend_id']
        loan.date_loaned = json_data['date_loaned']
        session.add(loan)
        session.commit()
        return jsonify({'status': 'Pomyślnie zaktualizowano dane wypożyczenia'})

@app.route('/loan/<int:id>', methods=['DELETE'])
def delete_loan(loan_id):
    loan = session.query(Loan).filter_by(id=loan_id).first()
    if loan is None:
        return jsonify({'status': 'Nie ma takiej pozyczki'})
    else:
        session.delete(loan)
        session.commit()
        return jsonify({'status': 'Pomyslnie usunueto pozyczke'})

