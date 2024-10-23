from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "unaclavesecreta"

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/procesa", methods=['POST'])
def procesa():
    fecha = request.form.get('fecha')
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    turno = request.form.get('turno')
    seminarios = request.form.getlist('seminarios')

    if not fecha or not nombre or not apellido or not turno:
        return "Error: Todos los campos son obligatorios", 400

    registro = {
        'fecha': fecha,
        'nombre': nombre,
        'apellido': apellido,
        'turno': turno,
        'seminarios': seminarios
    }

    if 'registro' not in session:
        session['registro'] = []

    session['registro'].append(registro)
    session.modified = True

    return redirect(url_for("lista"))

@app.route("/lista")
def lista():
    registros = session.get('registro', [])
    return render_template('lista.html', registros=registros)

@app.route("/eliminar/<int:index>")
def eliminar(index):
    try:
        del session['registro'][index]
        session.modified = True
    except IndexError:
        return "Error: El registro no existe", 400
    return redirect(url_for('lista'))

@app.route("/editar/<int:index>", methods=['GET', 'POST'])
def editar(index):
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        turno = request.form.get('turno')
        seminarios = request.form.getlist('seminarios')

        if not fecha or not nombre or not apellido or not turno:
            return "Error: Todos los campos son obligatorios", 400

        session['registro'][index] = {
            'fecha': fecha,
            'nombre': nombre,
            'apellido': apellido,
            'turno': turno,
            'seminarios': seminarios
        }
        session.modified = True
        return redirect(url_for('lista'))

    registro = session['registro'][index]
    return render_template('index.html', registro=registro, edit=True)

if __name__ == "__main__":
    app.run(debug=True)