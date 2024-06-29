from flask import Flask, redirect, request, jsonify, Blueprint
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from marshmallow import fields, validate, ValidationError
from flask_sqlalchemy import SQLAlchemy
import flask_email
import flask_migrate
import bcrypt
import flask_jwt


# Flask configurations and inheritances
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mainDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)









#define a schema model with ma and db

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

# Employe CRUD routes
@app.route('/employes', methods=['POST'])
def create_employe():
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
    return jsonify(new_employe.to_dict()), 201

@app.route('/employes', methods=['GET'])
def get_employes():
    employes = Employe.query.all()
    return jsonify([employe.to_dict() for employe in employes])

@app.route('/employes/<int:id>', methods=['GET'])
def get_employe(id):
    employe = Employe.query.get_or_404(id)
    return jsonify(employe.to_dict())

@app.route('/employes/<int:id>', methods=['PUT'])
def update_employe(id):
    data = request.get_json()
    employe = Employe.query.get_or_404(id)
    
    employe.UserName = data.get('UserName', employe.UserName)
    employe.email = data.get('email', employe.email)
    employe.address = data.get('address', employe.address)
    employe.img = data.get('img', employe.img)
    employe.expertees = data.get('expertees', employe.expertees)
    
    db.session.commit()
    return jsonify(employe.to_dict())

@app.route('/employes/<int:id>', methods=['DELETE'])
def delete_employe(id):
    employe = Employe.query.get_or_404(id)
    db.session.delete(employe)
    db.session.commit()
    return '', 204
