import flask
from flask import Flask
from flask import request
from flask import render_template
from flask import make_response
from flask_material import Material
from flask_wtf import CSRFProtect
from flask import g
from flask_login import LoginManager
from flask import Flask, session, redirect, url_for, escape, request
from flask_sqlalchemy import sqlalchemy
from flask import redirect
from flask import flash


import forms

app = Flask(__name__)
app.secret_key = 'any random string'

@app.before_request
def before_request():
    #Levntar conexión a la base de datos
    if 'userName' not in session:
        print('Anonymous User')

@app.after_request
def after_request(response):
    #Cerrar la conexión a la base de datos
    return response

@app.errorhandler(404)
def pageNotFound(error):
    if 'userName' in session:
        return redirect(url_for('showDashBoard'))
    else:
        return render_template('index.html')

@app.route('/')
def index():
    if 'userName' in session:
        return redirect(url_for('showDashBoard'))
    else:
        return render_template('index.html')

@app.route('/cookie')
def cookie():
    response = make_response(render_template('cookie.html'))
    response.set_cookie('custome_cookie', 'prueba')
    return response

@app.route('/logout')
def logout():
    if 'userName' in session:
        session.pop('userName')
    return redirect(url_for('index'))


@app.route('/AdminDashBoard')
def AdminDashBoard():
    return render_template('AdminDashBoard.ht')

@app.route('/dashboard')
def showDashBoard():
    if 'userName' in session:
        userName = session['userName']
        sucess_message = '{}'.format(userName)
        flash(sucess_message)

        return render_template('dashboard.html')
    else:
        return redirect(url_for('index'))


@app.route('/login', methods = ['GET', 'POST'])
def showLoginForm():
    if 'userName' in session:
            return redirect(url_for('showDashBoard'))
    else:
        loginForm = forms.loginForm(request.form)
        if request.method == 'POST' and loginForm.validate():
            session['userName'] = request.form['userName']
            session['password'] = request.form['password']
            username = loginForm.userName.data

            return redirect(url_for('showDashBoard'))

    return render_template('login.html', form = loginForm)

@app.route('/newMeet')
def showMeetings():
    return render_template('createMeeting.html')

if __name__ == '__main__':
    app.run(debug = True, port = 8000)
