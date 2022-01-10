from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bookshop.db"
db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'Book'
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author_firstName = db.Column(db.String(50))
    author_lastName = db.Column(db.String(50))
    genre = db.Column(db.String(50))
    price = db.Column(db.String(30))
    image = db.Column(db.String(100))
    orders = db.relationship('Order', backref=db.backref('Purchase'))

    def __str__(self):
        return f'{self.title} {self.author_firstName} {self.author_lastName} {self.genre} {self.price} {self.image}'
    

class Order(db.Model):
    __tablename__ = 'Order'
    order_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    address = db.Column(db.String(100))
    book_id = db.Column(db.Integer, db.ForeignKey('Book.book_id'))
    quantity = db.Column(db.Integer)

    def __str__(self):
        return f'{self.title} {self.author_firstName} {self.author_lastName} {self.genre} {self.price} {self.image}'


#db.create_all()

Franeknstein = Book(title="Frankenstein", author_firstName = "Mary", author_lastName = "Shelley", genre = "Horror", price = "30.00", image = 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Frankenstein_1818_edition_title_page.jpg/220px-Frankenstein_1818_edition_title_page.jpg')
Neuromancer = Book(title="Neuromancer", author_firstName = "William", author_lastName = "Gibson", genre = "Science Fiction", price = "18.00", image = 'https://upload.wikimedia.org/wikipedia/en/thumb/4/4b/Neuromancer_%28Book%29.jpg/220px-Neuromancer_%28Book%29.jpg')
Nineteen_Eighty_Four = Book(title="1984", author_firstName = "George", author_lastName = "Orwell", genre = "Dystopian", price = "20.00", image = 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/1984first.jpg/220px-1984first.jpg')
FullmetalAlchemist_Volumne1 = Book(title="Fullmetal Alchemist Volume 1", author_firstName = "Hiromu", author_lastName = "Arakawa", genre = "Manga", price = "6.25", image = 'https://upload.wikimedia.org/wikipedia/en/thumb/9/9d/Fullmetal123.jpg/220px-Fullmetal123.jpg')
Dracula = Book(title="Dracula", author_firstName = "Bram", author_lastName = "Stoker", genre = "Horror", price = "15.00", image = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Dracula_1st_ed_cover_reproduction.jpg/220px-Dracula_1st_ed_cover_reproduction.jpg')

#db.session.add(Franeknstein)
#db.session.add(Neuromancer)
#db.session.add(Nineteen_Eighty_Four)
#db.session.add(FullmetalAlchemist_Volumne1)
#db.session.add(Dracula)

def serialize_books(Book):
    return {
        'book_id': Book.book_id,
        'title': Book.title,
        'image': Book.image,
        'price': Book.price,
        'author_name': Book.author_firstName + ' ' + Book.author_lastName
    }

@app.route('/books', methods =['GET'])
def book_List():
    return jsonify([*map(serialize_books, Book.query.all())])

@app.route('/searchResult', methods = ['POST'])
def search_result():
    book_name = request.json["title"]
    result = Book.query.filter_by(title=book_name).first()
    exists = db.session.query(db.session.query(Book).filter_by(title=book_name).exists()).scalar()
    if (exists):
        return (jsonify(serialize_books(result)))
    else:
        return 'Book was not found.', 404

@app.route('/sendOrder', methods = ['POST'])
def receiveOrders():
    book_name = request.json["title"]
    customerFN = request.json["firstName"]
    customerLN = request.json["lastName"]
    customerState = request.json["state"]
    customerCity = request.json["city"]
    customerAddress = request.json["address"]
    quantity = request.json["quantity"]
    
    bookToOrder = Book.query.filter_by(title=book_name).first()
    
    orderedBook = Order(first_name=customerFN, last_name=customerLN, city=customerCity, state=customerState, address=customerAddress,Purchase=bookToOrder, quantity=quantity)
    db.session.add(orderedBook)
    db.session.commit()
    return 'Order received'

if __name__ == "__main__":
    app.run(debug=True)