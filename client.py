import argparse
import requests
from api import engine, Base


class BookClient():
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def get_all_books(self):
        r = requests.get(f'http://{self.host}:{self.port}/books')

    def get_book(self, id):
        r = requests.get(f'http://{self.host}:{self.port}/books/{id}')

    def add_book(self, book):
        r = requests.post(f'http://{self.host}:{self.port}/books', json=book)

    def update_book(self,id,book):
        r = requests.put(f'http://{self.host}:{self.port}/books/{id}',json=book)

    def delete_book(self, id):
        r = requests.delete(f'http://{self.host}:{self.port}/books/{id}')

    def get_friends(self):
        r = requests.get(f'http://{self.host}:{self.port}/friends')

    def get_friend(self, id):
        r = requests.get(f'http://{self.host}:{self.port}/friends/{id}')

    def add_friend(self, friend):
        r = requests.post(f'http://{self.host}:{self.port}/friends', json=friend)

    def update_friend(self, id, friend):
        r = requests.put(f'http://{self.host}:{self.port}/friends/{id}', json=friend)

    def delete_friend(self, id):
        r = requests.delete(f'http://{self.host}:{self.port}/friends/{id}')

    def get_loans(self):
        r = requests.get(f'http://{self.host}:{self.port}/loan')

    def get_loan(self, id):
        r = requests.get(f'http://{self.host}:{self.port}/loan/{id}')

    def add_loan(self, loan):
        r = requests.post(f'http://{self.host}:{self.port}/loan', json=loan)

    def update_loan(self, id, loan):
        r = requests.put(f'http://{self.host}:{self.port}/loan/{id}', json=loan)

    def delete_loan(self,id):
        r = requests.delete(f'http://{self.host}:{self.port}/loan/{id}')


Base.metadata.create_all(engine)
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title='Tables', dest='table')
client = BookClient('127.0.0.1', 5000)

parser_books = subparsers.add_parser('books', help='Operacje dla tabeli ksiazki')
group_books = parser_books.add_mutually_exclusive_group()
group_books.add_argument('--list', action='store_true', help='Lista wszystkich ksiazek')
group_books.add_argument('--add', action='store_true', help='Dodaj nowa ksiazke')
group_books.add_argument('--delete', action='store_true', help='Usun ksiazke')
parser_books.add_argument('--id', help='ID znajomego')
parser_books.add_argument('--title', help='Tytul ksiazki')
parser_books.add_argument('--author', help='Autor ksiazki')
parser_books.add_argument('--year', type=int, help='Rok wydania ksiazki')

parser_friends = subparsers.add_parser('friends', help='Operacje dla tabeli znajomi')
group_friends = parser_friends.add_mutually_exclusive_group()
group_friends.add_argument('--list', action='store_true', help='Lista wszystkich znajomych')
group_friends.add_argument('--add', action='store_true', help='Dodaj znajomego')
group_friends.add_argument('--delete', action='store_true', help='Usun znajomego')
parser_friends.add_argument('--id', help='ID znajomego')
parser_friends.add_argument('--name', help='Nazwa znajomego')
parser_friends.add_argument('--email', help='E-mail znajomego')

parser_loans = subparsers.add_parser('loans', help='Operacje dla tabeli wypozyczanie')
group_loans = parser_loans.add_mutually_exclusive_group()
group_loans.add_argument('--list', action='store_true', help='Lista wszystkich wypozyczen')
group_loans.add_argument('--add', action='store_true', help='Dodaj nowe wypozyczenie ksiazki')
group_loans.add_argument('--retur', action='store_true', help='Zwroc wypozyczona ksiazke')
parser_loans.add_argument('--id', type=int, help='ID pozyczki')
parser_loans.add_argument('--friend', type=int, help='ID znajomego')
parser_loans.add_argument('--book', type=int, help='ID ksiazki')

args = parser.parse_args()
if args.table == 'books':
    if args.list:
        client.get_all_books()
    elif args.add:
        client.add_book({"title" : args.title, "author" : args.author, "year" : args.year})
        print('Ksiazka zostala dodana pomyslnie')
    elif args.delete:
        client.delete_book(args.id)
        print("usunieto ksiazke")

elif args.table == 'friends':
    if args.list:
        client.get_friends()
    elif args.add:
        client.add_friend({"name" : args.name, "email" : args.email})
        print('Znajomy zostal dodany pomyslnie')
    elif args.delete:
        client.delete_friend(args.id)
        print("usunieto znajomego")
elif args.table == 'loans':
    if args.list:
        client.get_loans()
    elif args.add:
        client.add_loan({"friend_id" : args.friend, "book_id" : args.book})
        print('Wypozyczenie ksiazki zostalo dodane')
    elif args.retur:
        client.delete_loan({"friend_id" : args.friend})
        print('Zwrot ksiazki udany')