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
from models import UserRequest
from config import DevelopmentConfig

import forms

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

@app.before_request
def before_request():
    if 'userName' not in session and request.endpoint in ['logout','showDashBoard']:
        return redirect(url_for('index'))
    elif 'userName' in session and request.endpoint in['index','showLoginForm']:
        return redirect(url_for('showDashBoard'))


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
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('userName')
    return redirect(url_for('index'))

@app.route('/dashboard', methods = ['GET', 'POST'])
def showDashBoard():
    obtainUserName()
    return render_template('dashboard.html')


@app.route('/login', methods = ['GET', 'POST'])
def showLoginForm():
    loginForm = forms.loginForm(request.form)
    if request.method == 'POST' and loginForm.validate():
        username = request.form['userName']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()

        #if user is not None and user.verifyPassword(password):
        if 1==1:
            session['userName'] = username
            return redirect(url_for('showDashBoard'))


    return render_template('login.html', form = loginForm)

@app.route('/register', methods = ['GET','POST'])
def showRegisterForm():
    registerForm = forms.registerForm(request.form)
    if request.method == 'POST' and registerForm.validate():
        possibleUser   = UserRequest(registerForm.UserName.data,
                                     registerForm.Email.data   ,
                                     registerForm.Name.data    ,
                                     registerForm.LastName.data,
                                     registerForm.Password.data)

        db.session.add(possibleUser)
        db.session.commit()

        return redirect(url_for('showRegisterForm'))


    return render_template('registerpage.html', form = registerForm)

@app.route('/admindashboard')
def showAdminDashBoard():
    return render_template('adminDashBoard.html')

@app.route('/UsersRequests')
def UsersRequests():
    id = request.args.get('id', None)
    option = request.args.get('option', None)

    if id is not None and option is not None:

        if option == 'Approve':
            pass
        else:
            db.session.query(UserRequest).filter(UserRequest.idPerson==id).delete()
            db.session.commit()

    usersRequests = UserRequest.query.all()
    return render_template('usersRequests.html', usersRequests = usersRequests)

def obtainUserName():
    userName = session['userName']
    sucess_message = '{}'.format(userName)
    flash(sucess_message)

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port = 8000)
