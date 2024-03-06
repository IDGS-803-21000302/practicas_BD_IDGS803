from flask_sqlalchemy import SQLAlchemy
import datetime 

db=SQLAlchemy()

class Trabajadores(db.Model):
    __tablename__="alumnos"
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(200))
    email=db.Column(db.String(50))
    telefono=db.Column(db.String(10))
    direccion=db.Column(db.String(200))
    sueldo=db.Column(db.Float)
    create_date=db.Column(db.DateTime, default=datetime.datetime.now)


class Cliente(db.Model):
    __tablename__="Cliente"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    direccion = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    fecha_compra = db.Column(db.DateTime, default=datetime.datetime.now)

class Pizza(db.Model):
    __tablename__="Pizza"
    id = db.Column(db.Integer, primary_key=True)
    tamano = db.Column(db.String(50))
    precio = db.Column(db.Float)
    ingredientes = db.Column(db.String(255))
    id_cliente= db.Column(db.Integer)