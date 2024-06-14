from flask import abort
from flask import Flask, flash, session, redirect, url_for, request
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./autos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '84545hdjdfkh54'

users = [{'user': 'user', 'psw': 'psw'}]

class Auto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, title, status, price):
        self.title = title
        self.status = status
        self.price = price

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/add_auto', methods=['POST','GET'])
def edit():
    if request.method == "POST":
        title = request.form['title']
        status = request.form['status']
        price = request.form['price']
        service = Auto(title=title, status=status, price=price)
        try:
            db.session.add(service)
            db.session.commit()
            flash("Автомобиль добавлен", category='succes')
        except:
            flash("Ошибка добавления автомобиля", category='error')
    return render_template("add_auto.html")

@app.route('/cars')
def news():
    items = Auto.query.order_by(Auto.id).all()
    return render_template("cars.html", data=items)

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST' and {'user': request.form['username'], 'psw': request.form['psw']} in users:
        session['userlogged'] = request.form['username']
        return redirect(url_for('profile'))
    else:
        flash("Ошибка входа", category='error')
    return render_template('login.html')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Добавить авто':
            return redirect(url_for('edit'))
        elif request.form['submit_button'] == 'Выйти':
            session.clear()
            return redirect(url_for('login'))
    return render_template('profile.html')

if __name__ == "__main__":
    with app.app_context();
        db.create_all()
    app.run(debug=True)
