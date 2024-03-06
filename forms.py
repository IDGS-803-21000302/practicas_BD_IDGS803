from wtforms import Form
from wtforms import StringField, SelectField,RadioField,EmailField,IntegerField, FloatField,SelectMultipleField,SubmitField,HiddenField
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

class PizzaOrderForm(Form):
    # Datos del cliente
    nombre = StringField('Nombre Completo', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, message='Ingrese un nombre válido')
    ])
    direccion = StringField('Dirección', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, message='Ingrese una dirección válida')
    ])
    telefono = StringField('Teléfono', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=7, message='Ingrese un teléfono válido')
    ])
    fecha_compra = StringField('Fecha de Compra', [
        validators.DataRequired(message='El campo es requerido')
    ]) # Puedes usar un campo de tipo DateField si prefieres manejar la fecha directamente como un objeto de fecha.
    
    # Detalles de la pizza
    tamano_pizza = RadioField('Tamaño de Pizza', choices=[('chica', 'Chica $40'), ('mediana', 'Mediana $80'), ('grande', 'Grande $120')], validators=[validators.DataRequired()])
    ingredientes = SelectMultipleField('Ingredientes', choices=[('jamon', 'Jamón $10'), ('piña', 'Piña $10'), ('champinones', 'Champiñones $10')]) # La lista de choices probablemente venga de tu base de datos
    numero_pizzas = IntegerField('Número de Pizzas', [
        validators.DataRequired(message='El campo es requerido'),
        validators.NumberRange(min=1, message='Debe pedir al menos una pizza')
    ])
    agregar = SubmitField('Agregar')
    registrar = SubmitField('Registrar')
    csrf_token = HiddenField()