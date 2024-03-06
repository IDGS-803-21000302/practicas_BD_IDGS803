from wtforms import Form
from wtforms import StringField, SelectField,RadioField,EmailField,IntegerField, FloatField,BooleanField
from wtforms import validators


class UsersForm(Form):
    nombre = StringField('nombre',[
        validators.DataRequired(message='el campo es requerido'),
        validators.Length(min=4, max=20, message = 'ingresa nombre valido')
    ])

    apaterno = StringField('apaterno',[
        validators.DataRequired(message='el campo es requerido'),
        validators.Length( max=20, min=4, message = 'ingresa nombre valido')
    ])

    amaterno = StringField('amaterno',[
        validators.DataRequired(message='el campo es requerido'),
        validators.Length(min=4, max=20, message = 'ingresa nombre valido')
    ])

    edad = IntegerField('edad')

    correo = EmailField('correo',[
        validators.Email(message='Ingrese un corre valido')
    ])


class UsersForm2(Form):
    id=IntegerField('id')
    nombre = StringField('nombre',[
        validators.DataRequired(message='el campo es requerido'),
        validators.Length(min=4, max=20, message = 'ingresa nombre valido')
    ])

    
    email = EmailField('correo',[
        validators.Email(message='Ingrese un corre valido')
    ])

    telefono = IntegerField('Telefono')

    direccion = StringField('Direccion ')

    sueldo = FloatField('Sueldo')

class VentaForm(Form):
    id = IntegerField("id")
    nombre = StringField("nombre", [validators.DataRequired(message='el campo es requerido'), validators.length(min=4,max=10,message='ingresa nombre valido')])
    direccion = StringField("Direccion", [validators.DataRequired(message='el campo es requerido'), validators.length(min=4,max=10,message='ingresa direccion valida')])
    telefono = StringField("Telefono", [validators.DataRequired(message='el campo es requerido'), validators.length(min=4,max=10,message='ingresa telefono valido')])
    total = FloatField("Total", render_kw={'readonly': True})
    
class PizzaForm(Form):
    tamanioPizza = RadioField("Tamaño de Pizza", choices=[('chica','Chica $40'),('mediana','Mediana $80'),('grande','Grande $120')], default='chica')
    telefono = StringField("Telefono")
    jamon = BooleanField("Jamon $10")
    pinia = BooleanField("Piña $10")
    champinones = BooleanField("Champiñones $10")
    numero_pizzas = IntegerField("Numero de Pizzas", default=1)
    