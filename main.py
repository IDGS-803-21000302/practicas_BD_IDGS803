import datetime
from flask import Flask, render_template, request, flash, Response, url_for,session
from flask_wtf.csrf import CSRFProtect
from flask import redirect
from flask import g
from config import DevelopmentConfig
import forms

from models import db
from models import Trabajadores,Venta

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

@app.route('/pizzeria', methods=['GET', 'POST'])
def pizzeria():
    venta_form = forms.VentaForm(request.form)
    ventas = buscar_ventas_por_fecha(None)
    pizza_form = forms.PizzaForm(request.form)
    return render_template("ABC_Pizzeria.html", form = venta_form, pizza_form = pizza_form,ventas = ventas)

@app.route('/get-ventas')
def ventas():
    date_str = request.args.get('date')
    ventas = buscar_ventas_por_fecha(date_str)
    return redirect(url_for('pizzeria', ventas=ventas))

@app.route('/dispatch', methods=['POST'])
def dispatch():
    venta_form = forms.VentaForm(request.form)
    if request.method == "POST" and venta_form.validate():
        venta = Venta(nombre = venta_form.nombre.data, direccion = venta_form.direccion.data, telefono = venta_form.telefono.data, total = venta_form.total.data)
        db.session.add(venta)
        db.session.commit()
        flash("Se ha realizado la venta")
    return redirect(url_for('pizzeria'))

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

def buscar_ventas_por_fecha(date_str):
    try:
        if date_str is None:
            ventas = Venta.query.all()
        else:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            ventas = Venta.query.filter(Venta.created_date >= date).all()
        return ventas
    except ValueError:
        return "Formato de fecha no válido. Utiliza el formato YYYY-MM-DD", 400

if __name__== "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)

