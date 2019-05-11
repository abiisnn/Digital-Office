import flask
from flask import Flask
from flask import request
from flask import session
from flask import escape
from flask import flash
from flask import redirect
from flask import render_template
from flask import make_response
from flask import url_for
from flask import g
from flask_material import Material
from flask_wtf import CSRFProtect
from models import db
from models import User
from config import DevelopmentConfig

import forms

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

@app.before_request
def before_request():
    if 'userName' not in session:
        print('Anonymous User')

@app.after_request
def after_request(response):
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
        obtainUserName()

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

@app.route('/register', methods = ['GET','POST'])
def showRegisterForm():

    registerForm = forms.registerForm(request.form)

    if request.method == 'POST' and registerForm.validate():

        user      = User(registerForm.UserName.data,
                         registerForm.Email.data   ,
                         registerForm.Name.data    ,
                         registerForm.LastName.data,
                         registerForm.Employment.data,
                         registerForm.Office.data  ,
                         registerForm.Password.data)

        db.session.add(user)
        db.session.commit()

        sucess_message = 'Usuario registrado en la base de datos'
        flash(sucess_message)


    return render_template('registerpage.html', form = registerForm)


@app.route('/newMeet')
def showMeetings():
    return render_template('createMeeting.html')

@app.route('/MeetingMenu')
def showMeetingMenu():
    obtainUserName()
    return render_template('meetingspage.html')


def obtainUserName():
    userName = session['userName']
    sucess_message = '{}'.format(userName)
    flash(sucess_message)

if __name__ == '__main__':

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.run(port = 8000)
