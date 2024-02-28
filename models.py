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