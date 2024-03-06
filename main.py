import datetime
from flask import Flask, render_template, request, flash, Response, url_for,session
from flask_wtf.csrf import CSRFProtect
from flask import redirect
from flask import g
from config import DevelopmentConfig
import forms

from models import Pizza, db
from models import Trabajadores,Cliente

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.errorhandler(404)
def page_not_fund(e):
    return render_template('404.html'),404


@app.route("/index",methods=["GET","POST"])
def index():
    tra_form= forms.UsersForm2(request.form)
    if request.method=='POST':
        tra=Trabajadores(nombre=tra_form.nombre.data,
                     email=tra_form.email.data,
                     telefono=tra_form.telefono.data,
                     direccion=tra_form.direccion.data,
                     sueldo=tra_form.sueldo.data)
        db.session.add(tra)
        db.session.commit()
    return render_template("index.html",form=tra_form)

@app.route("/confirmar_pedido")
def confirmar_pedido():
    costo_total = request.args.get('costo_total', 0, type=float)
    return render_template("confirmar.html", costo_total=costo_total)

@app.route("/pedido", methods=["GET", "POST"])
def agregar_pedido():
    if 'pizzas' not in session:
        session['pizzas'] = []
    print('Hola')
    pedido_form = forms.PizzaOrderForm(request.form)
    if request.method == 'POST':
        if 'pizza' in request.form:  # Verifica si el botón presionado es "agregar"
            tamano_pizza = request.form.get('tamano_pizza')
            ingredientes = request.form.get('ingredientes')
            numero_pizzas = request.form.get('numero_pizzas')
            # Aquí podrías calcular el sub total basado en tu lógica de negocio
            sub_total = 0  # Supongamos que es 0 por ahora

            # Agrega la pizza a la lista en sesión
            session['pizzas'].append({
                'tamano': tamano_pizza,
                'ingredientes': ingredientes,
                'numero': numero_pizzas,
                'sub_total': sub_total
            })
            session.modified = True
        elif 'tn1' in request.form:
            print('entro')
            nuevo_cliente = Cliente(
                nombre=pedido_form.nombre.data,
                direccion=pedido_form.direccion.data,
                telefono=pedido_form.telefono.data
            )
            db.session.add(nuevo_cliente)
            db.session.flush()  # Esto es para obtener el ID del cliente antes de hacer commit
            costo_total=0
            for pizza in session['pizzas']:
                nueva_pizza = Pizza(
                    tamano=pizza['tamano'],
                    ingredientes=pizza['ingredientes'],
                    precio=0,  # Supongamos que aquí se calcula el precio real
                    id_cliente=nuevo_cliente.id
                )
                db.session.add(nueva_pizza)
                costo_total += nueva_pizza.precio  # Asumiendo que cada pizza tiene un precio ya definido

            db.session.commit()
            # Limpia las pizzas de la sesión después de registrar
            session.pop('pizzas', None)

            # Redireccionar a una ruta de confirmación con el costo total
            return redirect(url_for('confirmar_pedido', costo_total=costo_total))
            
            
    else:
        print('No entro')
        
        

    return render_template("pedidos.html", form=pedido_form,pizzas=session.get('pizzas', []))


@app.route("/ABC_Completo")
def ABC_Completo():
    tra_form=forms.UsersForm2(request.form)
    trabajador=Trabajadores.query.all()
    return render_template("ABC_Completo.html", trabajador=trabajador)

@app.route('/eliminar', methods=["GET", "POST"])
def eliminar():
    alum_form = forms.UsersForm2(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Trabajadores).filter(Trabajadores.id == id).first()
        if alum1:
            alum_form.id.data = id
            alum_form.nombre.data = alum1.nombre
            alum_form.email.data = alum1.email
            alum_form.telefono.data = alum1.telefono
            alum_form.direccion.data = alum1.direccion
            alum_form.sueldo.data = alum1.sueldo
        else:
            flash('No se encontró ningún trabajador con el ID proporcionado.', 'error')
            return redirect('ABC_Completo')
    if request.method == 'POST':
        id = alum_form.id.data
        alum = db.session.query(Trabajadores).get(id)
        if alum:
            db.session.delete(alum)
            db.session.commit()
            flash('El trabajador ha sido eliminado correctamente.', 'success')
            return redirect('ABC_Completo')
        else:
            flash('No se encontró ningún trabajador con el ID proporcionado.', 'error')
            return redirect('ABC_Completo')

    return render_template("eliminar.html", form=alum_form)



@app.route('/modificar', methods=["GET", "POST"])
def modificar():
    alum_form = forms.UsersForm2(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Trabajadores).filter(Trabajadores.id == id).first()
        if alum1:
            alum_form.id.data = id
            alum_form.nombre.data = alum1.nombre
            alum_form.email.data = alum1.email
            alum_form.telefono.data = alum1.telefono
            alum_form.direccion.data = alum1.direccion
            alum_form.sueldo.data = alum1.sueldo
        else:
            flash('No se encontró ningún trabajador con el ID proporcionado.', 'error')
            return redirect('ABC_Completo')

    if request.method == 'POST':
        id = alum_form.id.data
        alum1 = db.session.query(Trabajadores).filter(Trabajadores.id == id).first()
        if alum1:
            alum1.nombre = alum_form.nombre.data
            alum1.email = alum_form.email.data
            alum1.telefono = alum_form.telefono.data
            alum1.direccion = alum_form.direccion.data
            alum1.sueldo = alum_form.sueldo.data
            db.session.commit()
            flash('Los datos del trabajador han sido actualizados correctamente.', 'success')
            return redirect('ABC_Completo')
        else:
            flash('No se encontró ningún trabajador.', 'error')
            return redirect('ABC_Completo')

    return render_template("modificar.html", form=alum_form)


@app.route("/alumnos",methods=["GET","POST"])
def alum():
    nom=''
    apa=''
    ama=''
    mensaje=''
    alum_form= forms.UsersForm(request.form)
    if request.method=='POST' and alum_form.validate():
        nom=alum_form.nombre.data
        apa=alum_form.apaterno.data
        ama=alum_form.amaterno.data

        mensaje='Bienvenido {}'.format(nom)
        flash(mensaje)

        print("Nombre: {}".format(nom))
        print("Apa: {}".format(apa))
        print("Ama: {}".format(ama))
        
    return render_template("alumnos.html",form=alum_form,nom=nom,apa=apa,ama=ama)


if __name__== "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)

