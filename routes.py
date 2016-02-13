from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from functools import wraps
import sqlite3

DATABASE = 'sales.db'

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'to je ena skrivnost velika'

# database connection
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# funcija za dekorator login_required
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to log in first -  Najprej je potrebna prijava')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/hello')
@login_required
def hello():
    g.db = connect_db()
    cur = g.db.execute('SELECT name, amount FROM reps')
    sales = [dict(name=row[0], amount=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template('hello.html', sales=sales)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials! Please try again'
        else:
            session['logged_in'] = True
            return redirect(url_for('hello'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out  Odjava OK ')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

