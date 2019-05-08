from flask import Flask
from flask import request
from flask import render_template
from flask import make_response
from flask_material import Material
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask import Flask, session, redirect, url_for, escape, request
from flask_sqlalchemy import sqlalchemy
from flask import redirect
from flask import flash
import forms

app = Flask(__name__)
app.secret_key = 'any random string'


@app.route('/')
def index():
    if 'userName' in session:
        userName = session['userName']
        print(userName)
    return render_template('index.html')

@app.route('/cookie')
def cookie():
    response = make_response(render_template('cookie.html'))
    response.set_cookie('custome_cookie', 'prueba')
    return response

@app.route('/logout')
def logout():
    if 'userName' in session:
        pass
    return redirect(url_for('login'))

@app.route('/dashboard')
def showDashBoard():
    return render_template('dashboard.html')

@app.route('/login', methods = ['GET', 'POST'])
def showLoginForm():
    loginForm = forms.loginForm(request.form)

    if request.method == 'POST' and loginForm.validate():
        session['userName'] = request.form['userName']
        session['password'] = request.form['password']
        username = loginForm.userName.data
        sucess_message = 'Bienvenido {}'.format(username)
        flash(sucess_message)

        return redirect(url_for('showDashBoard'))

    return render_template('login.html', form = loginForm)

if __name__ == '__main__':
    app.run(debug = True, port = 8000)
