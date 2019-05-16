import flask
import threading
from flask_mail import Mail
from flask_mail import Message
from flask import Flask
from flask import request
from flask import session
from flask import escape
from flask import flash
from flask import redirect
from flask import render_template
from flask import make_response
from flask import url_for
from flask import copy_current_request_context
from flask import g
from flask_material import Material
from flask_wtf import CSRFProtect

#from models import db
#from models import User
#from models import UserRequest

from ModelV1 import db
from ModelV1 import User


from config import DevelopmentConfig
#from Crypto.Signature import PKCS1_v1_5
#from Crypto.Hash import SHA256
#from Crypto.PublicKey import RSA

import forms

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
mail = Mail()

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
        return render_template('General/index.html')

@app.route('/')
def index():
    return render_template('General/index.html')

@app.route('/logout')
def logout():
    session.pop('userName')
    return redirect(url_for('index'))

@app.route('/dashboard', methods = ['GET', 'POST'])
def showDashBoard():
    obtainUserName()
    return render_template('Employee/dashboard.html')


@app.route('/login', methods = ['GET', 'POST'])
def showLoginForm():
    loginForm = forms.loginForm(request.form)
    if request.method == 'POST' and loginForm.validate():
        username = request.form['userName']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()

        if user is not None and user.verifyPassword(password):
        #if 1==1:
            session['userName'] = username
            return redirect(url_for('showDashBoard'))


    return render_template('General/login.html', form = loginForm)

@app.route('/register', methods = ['GET','POST'])
def showRegisterForm():
    registerForm = forms.registerForm(request.form)
    if request.method == 'POST' and registerForm.validate():

        possibleUser   = User(registerForm.UserName.data,
                              registerForm.Email.data,
                              registerForm.Name.data,
                              registerForm.LastName.data,
                              registerForm.Password.data,
                              )

        db.session.add(possibleUser)
        db.session.commit()

        return redirect(url_for('showRegisterForm'))


    return render_template('RH/registerpage.html', form = registerForm)

@app.route('/admindashboard')
def showAdminDashBoard():
    return render_template('CEO/adminDashBoard.html')
@app.route('/newMeet')
def showMeet():
    return render_template('CEO/createMeeting.html')

@app.route('/UsersRequests')
def UsersRequests():
    id = request.args.get('id', None)
    option = request.args.get('option', None)

    if id is not None and option is not None:

        if option == 'Approve':

            userToAdd = db.session.query(UserRequest).filter(UserRequest.idPerson==id)

            row = userToAdd[0]

            user      =  User(row.username,
                              row.email,
                              row.name,
                              row.lastName,
                              "asasasasa",
                              row.password)

            #key = RSA.generate(1024)

            #privateKey = key.exportKey()
            #publicKey  = key.publickey().exportKey()
            #f1 = open('privateKey.txt','w')
            #f2 = open('publicKey.txt' ,'w')
            #f1.write(str(privateKey))
            #f2.write(str(publicKey))
            #f1.close()
            #f2.close()



            @copy_current_request_context
            def sendMessage(userEmail, userName,name):
                sendEmail(userEmail,userName,name)

            sender = threading.Thread(name='mail_sender',target=sendMessage, args=(row.email,row.username,row.name))
            sender.start()

            db.session.add(user)

        db.session.query(UserRequest).filter(UserRequest.idPerson==id).delete()

        db.session.commit()

    usersRequests = UserRequest.query.all()

    return render_template('CEO/usersRequests.html', usersRequests = usersRequests)

def obtainUserName():
    userName = session['userName']
    sucess_message = '{}'.format(userName)
    flash(sucess_message)

def sendEmail(userEmail, userName,name):
    msg = Message('Status of your request',
                   sender = app.config['MAIL_USERNAME'],
                   recipients = [userEmail]
                  )

    msg.html = render_template('General/email.html', name = name, userName = userName)

    with app.open_resource("static/img/logo2.png") as fp:
        msg.attach("logo2.png", "logo2/png", fp.read())

    mail.send(msg)

if __name__ == '__main__':
    db.init_app(app)
    mail.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port = 8001)
