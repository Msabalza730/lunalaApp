import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class MedicineStocks(db.Model):
    __tablename__ = 'medicine'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    stock = db.Column(db.String(200))
    due_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, name, stock, due_date):
        self.name = name
        self.stock = stock
        self.due_date = due_date


class Animal(db.Model):
    __tablename__ = 'animal'
    id = db.Column(db.Integer, primary_key=True)
    animal = db.Column(db.String(200))
    breed = db.Column(db.String(200))

    def __init__(self, animal, breed):
        self.animal = animal
        self.breed = breed


class FoodStocks(db.Model):
    __tablename__ = 'food'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(200))
    stock = db.Column(db.String(200))
    due_date = db.Column(db.DateTime, nullable=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.animal'), nullable=False)

    def __init__(self, brand, stock, due_date, animal_id):
        self.brand = brand
        self.stock = stock
        self.due_date = due_date
        self.animal_id = animal_id
