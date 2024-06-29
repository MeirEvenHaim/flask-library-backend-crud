from flask import Flask, redirect, request, jsonify, Blueprint
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.exceptions import HTTPException
from datetime import datetime
from sqlalchemy.orm import relationship

# Flask configurations and inheritances
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mainDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)






#**********************************loan*******************************
# Define the Loan model
class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    # Relationships
    user = db.relationship('User', backref=db.backref('loans', lazy=True))
    admin = db.relationship('Admin', backref=db.backref('loans', lazy=True))
    book = db.relationship('Book', backref=db.backref('loans', lazy=True))

    def __repr__(self):
        return f"<Loan(id={self.id}, loan_date='{self.loan_date}', user_id={self.user_id}, user_name='{self.user.UserName}', admin_id={self.admin_id}, admin_name='{self.admin.UserName}', book_id={self.book_id}, book_name='{self.book.book_name}')>"



    def to_dict(self):
        return {
            'id': self.id,
            'loan_date': self.loan_date.isoformat(),
            'user_id': self.user_id,
            'user_name': self.user.UserName,
            'admin_id': self.admin_id,
            'admin_name': self.admin.UserName,
            'book_id': self.book_id,
            'book_name': self.book.book_name
        }



# Define the Employe model
class Employe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(25), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=False, nullable=False)
    address = db.Column(db.String(120), unique=False, nullable=False)
    img = db.Column(db.String(), unique=False)
    expertees = db.Column(db.String(30), unique=False, nullable=False)

    def __repr__(self):
        return f"<Employe(id={self.id}, email='{self.email}', img='{self.img}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'UserName': self.UserName,
            'email': self.email,
            'address': self.address,
            'img': self.img,
            'expertees': self.expertees
        }








# Define the Register model
class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(25), unique=True, nullable=True)
    password = db.Column(db.String(128), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f"<Register(id={self.id}, email='{self.email}', UserName='{self.UserName}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'UserName': self.UserName,
            'email': self.email,
            'password': self.password
        }












# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(25), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(128), unique=False, nullable=False)
    address = db.Column(db.String(120), unique=False, nullable=False)
    img = db.Column(db.String(100), unique=False)

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', img='{self.img}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'UserName': self.UserName,
            'email': self.email,
            'password': self.password,
            'address': self.address,
            'img': self.img
        }








# Define the Admin model
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(25), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(128), unique=False, nullable=False)
    address = db.Column(db.String(120), unique=False, nullable=False)
    authorety_level = db.Column(db.Integer, unique=False, nullable=False)
    img = db.Column(db.String(100), unique=False)

    def __repr__(self):
        return f"<Admin(id={self.id}, email='{self.email}', authorety_level='{self.authorety_level}', img='{self.img}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'UserName': self.UserName,
            'email': self.email,
            'password': self.password,
            'address': self.address,
            'authorety_level': self.authorety_level,
            'img': self.img
        }

# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(25), unique=True, nullable=True)
    author = db.Column(db.String(120), unique=False, nullable=False)
    date_of_publish = db.Column(db.Integer, unique=False, nullable=False)
    series = db.Column(db.String(120), unique=False, nullable=False)
    readers_age = db.Column(db.Integer, unique=False, nullable=False)
    img = db.Column(db.String(100), unique=False, nullable=True)

    def __repr__(self):
        return f"<Book(id={self.id}, author='{self.author}', series='{self.series}', img='{self.img}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'book_name': self.book_name,
            'author': self.author,
            'date_of_publish': self.date_of_publish,
            'series': self.series,
            'readers_age': self.readers_age,
            'img': self.img
        }


#werkzug http exception method in a function validation 

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return jsonify({'error': e.description}), e.code
    return jsonify({'error': str(e)}), 500
    
    
    
## a format function that response depends on the problem inside the data /error/messege provided
def format_response(data=None, error=None, message=None):
    response = {}
    if data is not None:
        response['data'] = data
    if error is not None:
        response['error'] = error
    if message is not None:
        response['message'] = message
    return jsonify(response)
    
    
    
#***************loan crud*********************

@app.route('/loans', methods=['POST'])
def create_loan():
    try:
        data = request.get_json()
        new_loan = Loan(
            user_id=data['user_id'],
            admin_id=data['admin_id'],
            book_id=data['book_id']
        )
        db.session.add(new_loan)
        db.session.commit()
        return jsonify(new_loan.to_dict()), 201
    except Exception as e:
        return jsonify(error=str(e)), 400
        
@app.route('/loans', methods=['GET'])
def get_loans():
    try:
        loans = Loan.query.all()
        return jsonify([loan.to_dict() for loan in loans])
    except Exception as e:
        return jsonify(error=str(e)), 500
        
        
@app.route('/loans/<int:id>', methods=['GET'])
def get_loan(id):
    try:
        loan = Loan.query.get(id)
        if loan is None:
            return jsonify(error='Loan not found'), 404
        return jsonify(loan.to_dict())
    except Exception as e:
        return jsonify(error=str(e)), 500
        
@app.route('/loans/<int:id>', methods=['PUT'])
def update_loan(id):
    try:
        data = request.get_json()
        loan = Loan.query.get(id)
        if loan is None:
            return jsonify(error='Loan not found'), 404
        
        loan.user_id = data.get('user_id', loan.user_id)
        loan.admin_id = data.get('admin_id', loan.admin_id)
        loan.book_id = data.get('book_id', loan.book_id)
        
        db.session.commit()
        return jsonify(loan.to_dict())
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/loans/<int:id>', methods=['DELETE'])
def delete_loan(id):
    try:
        loan = Loan.query.get(id)
        if loan is None:
            return jsonify(error='Loan not found'), 404
        db.session.delete(loan)
        db.session.commit()
        return '', 204
    except Exception as e:
        return jsonify(error=str(e)), 400


# Employe CRUD routes
@app.route('/employes', methods=['POST'])
def create_employe():
    try:
        data = request.get_json()
        new_employe = Employe(
            UserName=data.get('UserName'),
            email=data.get('email'),
            address=data.get('address'),
            img=data.get('img'),
            expertees=data.get('expertees')
        )
        db.session.add(new_employe)
        db.session.commit()
        return format_response(new_employe.to_dict()), 201
    except Exception as e:
        return format_response(error=str(e)), 400

@app.route('/employes', methods=['GET'])
def get_employes():
    try:
        employes = Employe.query.all()
        return format_response([employe.to_dict() for employe in employes])
    except Exception as e:
        return format_response(error=str(e)), 500

@app.route('/employes/<int:id>', methods=['GET'])
def get_employe(id):
    try:
        employe = Employe.query.get(id)
        if employe is None:
            return format_response(error='Employe not found'), 404
        return format_response(employe.to_dict())
    except Exception as e:
        return format_response(error=str(e)), 500

@app.route('/employes/<int:id>', methods=['PUT'])
def update_employe(id):
    try:
        data = request.get_json()
        employe = Employe.query.get(id)
        if employe is None:
            return format_response(error='Employe not found'), 404
        
        employe.UserName = data.get('UserName', employe.UserName)
        employe.email = data.get('email', employe.email)
        employe.address = data.get('address', employe.address)
        employe.img = data.get('img', employe.img)
        employe.expertees = data.get('expertees', employe.expertees)
        
        db.session.commit()
        return format_response(employe.to_dict())
    except Exception as e:
        return format_response(error=str(e)), 400

@app.route('/employes/<int:id>', methods=['DELETE'])
def delete_employe(id):
    try:
        employe = Employe.query.get(id)
        if employe is None:
            return format_response(error='Employe not found'), 404
        db.session.delete(employe)
        db.session.commit()
        return '', 204
    except Exception as e:
        return format_response(error=str(e)), 400

# Register CRUD routes ...
@app.route('/register', methods=['POST'])
def create_register():
    try:
        data = request.get_json()
        new_register = Register(
            UserName=data['UserName'],
            email=data['email'],
            password=data['password']
        )
        db.session.add(new_register)
        db.session.commit()
        return format_response(new_register.to_dict()), 201
    except Exception as e:
        return format_response(error=str(e)), 400

@app.route('/registers', methods=['GET'])
def get_registers():
    try:
        registers = Register.query.all()
        return format_response([register.to_dict() for register in registers])
    except Exception as e:
        return format_response(error=str(e)), 500

@app.route('/register/<int:id>', methods=['GET'])
def get_register(id):
    try:
        register = Register.query.get(id)
        if register is None:
            return format_response(error='Register not found'), 404
        return format_response(register.to_dict())
    except Exception as e:
        return format_response(error=str(e)), 500

@app.route('/register/<int:id>', methods=['PUT'])
def update_register(id):
    try:
        data = request.get_json()
        register = Register.query.get(id)
        if register is None:
            return format_response(error='Register not found'), 404
        register.UserName = data['UserName']
        register.email = data['email']
        register.password = data['password']
        db.session.commit()
        return format_response(register.to_dict())
    except Exception as e:
        return format_response(error=str(e)), 400

@app.route('/register/<int:id>', methods=['DELETE'])
def delete_register(id):
    try:
        register = Register.query.get(id)
        if register is None:
            return format_response(error='Register not found'), 404
        db.session.delete(register)
        db.session.commit()
        return format_response(message='Register deleted successfully')
    except Exception as e:
        return format_response(error=str(e)), 400

# User CRUD routes ...
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(
            UserName=data['UserName'],
            email=data['email'],
            password=data['password'],
            address=data['address'],
            # img=data.get('img')  # Use .get() to avoid KeyError if 'img' is not provided
        )
        db.session.add(new_user)
        db.session.commit()
        return format_response(new_user.to_dict()), 201
    except Exception as e:
        return format_response(error=str(e)), 400

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.get_json()
        user = User.query.get(id)
        if user is None:
            return format_response(error='User not found'), 404
        user.UserName = data.get('UserName', user.UserName)
        user.email = data.get('email', user.email)
        user.password = data.get('password', user.password)
        user.address = data.get('address', user.address)
        user.img = data.get('img', user.img)
        db.session.commit()
        return format_response(user.to_dict())
    except Exception as e:
        return format_response(error=str(e)), 400

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get(id)
        if user is None:
            return format_response(error='User not found'), 404
        db.session.delete(user)
        db.session.commit()
        return format_response(message='User deleted successfully')
    except Exception as e:
        return format_response(error=str(e)), 400

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.get(id)
        if user is None:
            return format_response(error='User not found'), 404
        return format_response(user.to_dict())
    except Exception as e:
        return format_response(error=str(e)), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return format_response([user.to_dict() for user in users])
    except Exception as e:
        return format_response(error=str(e)), 500

# Admin CRUD routes ...
@app.route('/admins', methods=['POST'])
def create_admin():
    try:
        data = request.get_json()
        new_admin = Admin(
            UserName=data['UserName'],
            email=data['email'],
            password=data['password'],
            address=data['address'],
            authorety_level=data['authorety_level']
        )
        db.session.add(new_admin)
        db.session.commit()
        return format_response(new_admin.to_dict()), 201
    except Exception as e:
        return format_response(error=str(e)), 400

@app.route('/admins', methods=['GET'])
def get_admins():
    try:
        admins = Admin.query.all()
        return format_response([admin.to_dict() for admin in admins])
    except Exception as e:
        return format_response(error=str(e)), 500

@app.route('/admins/<int:id>', methods=['GET'])
def get_admin(id):
    try:
        admin = Admin.query.get(id)
        if admin is None:
            return format_response(error='Admin not found'), 404
        return format_response(admin.to_dict())
    except Exception as e:
        return format_response(error=str(e)), 500

@app.route('/admins/<int:id>', methods=['PUT'])
def update_admin(id):
    try:
        data = request.get_json()
        admin = Admin.query.get(id)
        if admin is None:
            return format_response(error='Admin not found'), 404
        admin.UserName = data['UserName']
        admin.email = data['email']
        admin.password = data['password']
        admin.address = data['address']
        admin.authorety_level = data['authorety_level']
        db.session.commit()
        return format_response(admin.to_dict())
    except Exception as e:
        return format_response(error=str(e)), 400

@app.route('/admins/<int:id>', methods=['DELETE'])
def delete_admin(id):
    try:
        admin = Admin.query.get(id)
        if admin is None:
            return format_response(error='Admin not found'), 404
        db.session.delete(admin)
        db.session.commit()
        return format_response(message='Admin deleted successfully')
    except Exception as e:
        return format_response(error=str(e)), 400

# Book CRUD routes
@app.route('/books', methods=['POST'])
def create_book():
    try:
        data = request.get_json()
        new_book = Book(
            book_name=data['book_name'],
            author=data['author'],
            date_of_publish=data['date_of_publish'],
            series=data['series'],
            readers_age=data['readers_age'],
            img=data.get('img')
        )
        db.session.add(new_book)
        db.session.commit()
        return format_response(new_book.to_dict()), 201
    except Exception as e:
        return format_response(error=str(e)), 400

@app.route('/books', methods=['GET'])
def get_books():
    try:
        books = Book.query.all()
        return format_response([book.to_dict() for book in books])
    except Exception as e:
        return format_response(error=str(e)), 500

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    try:
        book = Book.query.get(id)
        if book is None:
            return format_response(error='Book not found'), 404
        return format_response(book.to_dict())
    except Exception as e:
        return format_response(error=str(e)), 500

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    try:
        data = request.get_json()
        book = Book.query.get(id)
        if book is None:
            return format_response(error='Book not found'), 404
        
        book.book_name = data.get('book_name', book.book_name)
        book.author = data.get('author', book.author)
        book.date_of_publish = data.get('date_of_publish', book.date_of_publish)
        book.series = data.get('series', book.series)
        book.readers_age = data.get('readers_age', book.readers_age)
        book.img = data.get('img', book.img)
        
        db.session.commit()
        return format_response(book.to_dict())
    except Exception as e:
        return format_response(error=str(e)), 400

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    try:
        book = Book.query.get(id)
        if book is None:
            return format_response(error='Book not found'), 404
        db.session.delete(book)
        db.session.commit()
        return format_response(message='Book deleted successfully')
    except Exception as e:
        return format_response(error=str(e)), 400



if __name__ == "__main__":
    # Create the database
    with app.app_context():
        db.create_all()
    app.run(debug=True)
