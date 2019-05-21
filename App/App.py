import flask
import threading
from flask import send_file
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
from ModelV1 import Meeting
from ModelV1 import Rel_Meeting_User
from ModelV1 import Memo
from ModelV1 import Rel_Memo_User
from config import DevelopmentConfig
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

import forms
import os

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
mail = Mail()
#Meeting
recipientsOfTheMeeting = {}
# recipientsInCharge = {}
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


#Memorandum
recipientsOfTheMemorandum = {}
memorandumSubject = ""
memorandumBody = ""
memorandumType = ""


@app.route('/comboEvent')
def comboEvent():
    Mtype = request.args.get('Mtype', None)

    if Mtype == '1':
        users = User.query.all()
        recipientsOfTheMemorandum.clear()
        for user in users:
            id = int(user.idPerson)
            recipientsOfTheMemorandum[id] = user

    else:
        print("limpiar")
        recipientsOfTheMemorandum.clear()

    return redirect(url_for('emitMemorandum', Mtype = Mtype))


@app.route('/upload', methods = ['POST','GET'])
def upload():
    target = os.path.join(APP_ROOT,'temporaryFolder/')
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        filename = file.filename
        print(filename)
        destination = "/".join([target,filename])
        file.save(destination)

    return redirect(url_for('emitMemorandum'))



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

@app.route('/deleteEmployee')
def deleteEmployee():
    id = request.args.get('id', None)
    user = db.session.query(User).filter(User.idPerson == id).delete()
    db.session.commit()
    return redirect(url_for('generateKeys'))

@app.route('/meetings')
def meetings():
    obtainUserName()
    return render_template('meetings.html')

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
    mtngs = Meeting.query.all()
    rel_mtngs = Rel_Meeting_User.query.all()
    val = session['idP']
    memos = Memo.query.all()
    rel_memo = Rel_Memo_User.query.all()
    return render_template('Employee/dashboard.html',meetings = mtngs,rel_m_u = rel_mtngs,idP=val,memo = memos,rel_memo = rel_memo)


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
            session['idP'] = user.idPerson
            print(user.position)
            return redirect(url_for('showDashBoard'))


    return render_template('General/login.html', form = loginForm)

@app.route('/register', methods = ['GET','POST'])
def showRegisterForm():
    flag = False
    registerForm = forms.registerForm(request.form)
    #select = request.form.get('comboBox')
    #print(str(select))
    if request.method == 'POST' and registerForm.validate():
        select = request.form.get('comboBox')

        possibleUser   = User(registerForm.UserName.data,
                              registerForm.Email.data,
                              registerForm.Name.data,
                              registerForm.LastName.data,
                              registerForm.Password.data,
                              str(select)
                              )

        flag = True
        db.session.add(possibleUser)
        db.session.commit()


    return render_template('RH/registerpage.html', form = registerForm, flag = flag)

@app.route('/admindashboard')
def showAdminDashBoard():
    mtngs = Meeting.query.all()
    rel_mtngs = Rel_Meeting_User.query.all()
    memos = Memo.query.all()
    rel_memo = Rel_Memo_User.query.all()
    return render_template('CEO/adminDashBoard.html',meetings = mtngs,rel_m_u = rel_mtngs,memo = memos,rel_memo = rel_memo)

@app.route('/emitBill')
def emitBill():
    return render_template('Employee/bill.html')



@app.route('/removeAll')
def removeAll():
    recipientsOfTheMemorandum.clear()
    return redirect(url_for('emitMemorandum'))

@app.route('/removeUser')
def removeUser():
    id = request.args.get('id', None)
    del recipientsOfTheMemorandum[int(id)]
    return redirect(url_for('emitMemorandum'))



@app.route('/emitmemorandum', methods = ['GET','POST'])
def emitMemorandum():
    Mtype = request.args.get('Mtype', None)
    global recipientsOfTheMemorandum
    global memorandumSubject
    global memorandumBody
    global memorandumType

    flag = False

    users = User.query.all()
    username = ""

    if request.method == 'POST':
        
        data = User.query.filter_by(username = request.form.get('searchField')).first()

        memorandumSubject = str(request.form.get('subject'))       .strip()
        memorandumType    = str(request.form.get('memorandumType')).strip()
        memorandumBody    = str(request.form.get('body'))          .strip()
        privateKey        =  request.files.getlist("file")

        print(memorandumSubject)
        print(memorandumType)
        print(memorandumBody)
        print(privateKey)

        if memorandumType is not None and len(memorandumSubject) > 0 and len(memorandumBody) > 0 and privateKey is not None and not data:
            if privateKey is not None:
                target = os.path.join(APP_ROOT,'temporaryFolder/')
                if not os.path.isdir(target):
                    os.mkdir(target)
                for file in request.files.getlist("file"):
                    filename = file.filename
                    print(filename)
                    destination = "/".join([target,filename])
                    file.save(destination)
                    flag = True
            memorandumType = memorandumType.split("=")[1]
            new_memo = Memo(memorandumSubject,memorandumType,1,memorandumBody)
            db.session.add(new_memo)
            db.session.commit()

            if memorandumType is not "1":
                records = Memo.query.all()
                lastMemo = -1
                for r in records:
                    lastMemo = r.idMemo

                for k in recipientsOfTheMemorandum:
                    relation = Rel_Memo_User(k,lastMemo)
                    db.session.add(relation)
                    db.session.commit()

        if data:
            if data.idPerson not in recipientsOfTheMemorandum.keys():
                recipientsOfTheMemorandum[data.idPerson] = data

    return render_template('CEO/emitMemorandum.html', users = users, dictionary = recipientsOfTheMemorandum, flag = flag, Mtype = Mtype)


@app.route('/rhdashboard')
def showRHDashBoard():
    return render_template('RH/RHDashboard.html')

asunto = ""
fecha = ""

@app.route('/newMeet', methods = ['GET', 'POST'])
def showMeet():
    users = User.query.all()
    global asunto
    global fecha
    global recipientsOfTheMeeting

    if request.method == 'POST':
        userInCharge = request.form.get('inCharge')
        asunto = request.form.get('asunto')
        fecha = request.form.get('fecha')
        if userInCharge is not None:
            print(recipientsOfTheMeeting) #Users will be part in the meeting
            print(userInCharge) #User in charge of the meeting
            print(asunto) #User in charge of the meeting
            print(fecha) #User in charge of the meeting]

            aux = User.query.filter_by(username = userInCharge).first()
            newMeeting = Meeting(aux.idPerson,asunto,fecha,"ruta")

            db.session.add(newMeeting)
            db.session.commit()


            records = Meeting.query.all()
            currMeeting = -1
            for r in records:
                currMeeting = r.idMeeting

            for k in recipientsOfTheMeeting:
                relation = Rel_Meeting_User(k,currMeeting)
                db.session.add(relation)
                db.session.commit()

            recipientsOfTheMeeting = {}
            asunto=""
            fecha=""
        else:
            username = request.form.get('searchField')
            print(username)
            if username is not "":
                data = User.query.filter_by(username = username).first()
                if data:
                    if data.idPerson not in recipientsOfTheMeeting.keys():
                        recipientsOfTheMeeting[data.idPerson] = data
            else:
                recipientsOfTheMeeting = {}

    else:#Aqui va a ser un get para los demas
        recipientsOfTheMeeting = {}
        asunto=""
        fecha=""
        #print('Otro metodo')
    return render_template('CEO/createMeeting.html', users = users, dictionary = recipientsOfTheMeeting)


@app.route('/generatekeys')
def generateKeys():
    users = User.query.all()
    id = request.args.get('id', None)


    _users = db.session.query(User).filter(User.idPerson == id)

    print(_users)
    for user in _users:

        if user.status == 1:
            key = RSA.generate(1024)
            privateKey = key.exportKey()
            publicKey  = key.publickey().exportKey()

            userName = str(user.username)

            fileName_prk = 'privateKeys/'+userName+"_privateKey.txt"
            fileName_puk = 'publicKeys/'+userName+"_publicKey.txt"

            file = open(fileName_prk,'w')
            file.write(str(privateKey))
            file.close()

            _file = open(fileName_puk, 'w')
            _file.write(str(publicKey))
            _file.close()

            _user = db.session.query(User).filter(User.idPerson == id).one()
            _user.publicKey = fileName_puk
            db.session.commit()

            return send_file(fileName_prk, as_attachment=True)


    return render_template('RH/generatekeys.html', users = users)


@app.route('/UsersRequests')
def UsersRequests():
    id = request.args.get('id', None)
    option = request.args.get('option', None)

    if id is not None and option is not None:

        if option == 'Approve':

            a_user = db.session.query(User).filter(User.idPerson == id).one()
            a_user.status = 1

            @copy_current_request_context
            def sendMessage(userEmail, userName,name):
                sendEmail(userEmail,userName,name)

            sender = threading.Thread(name='mail_sender',target=sendMessage, args=(a_user.email,a_user.username,a_user.name))
            sender.start()

        elif option == 'Reject':

            a_user = db.session.query(User).filter(User.idPerson == id).delete()

        db.session.commit()

    usersRequests = User.query.all()

    return render_template('CEO/usersRequests.html', usersRequests = usersRequests)

@app.route('/binnacle')
def binnacle():
    return render_template('RH/binnacle.html')


@app.route('/meetingList')
def meetingL():
    return render_template('General/meetingList.html')


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
    mail.send(msg)

@app.route('/EmeetingList')
def EmeetingList():
    obtainUserName()
    m = Meeting.query.all()
    rel = Rel_Meeting_User.query.all()
    val = session['idP']
    u = User.query.all()
    return render_template('Employee/meetingList.html',meetings = m,rel = rel, users = u,idP = val)

@app.route('/CEOmeetingList')
def CEOmeetingList():
    m = Meeting.query.all()
    rel = Rel_Meeting_User.query.all()
    u = User.query.all()
    return render_template('CEO/meetingList.html',meetings = m,rel = rel, users = u,idP = 1)

@app.route('/RHmeetingList')
def RHmeetingList():
    return render_template('RH/meetingList.html')


if __name__ == '__main__':
    db.init_app(app)
    mail.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port = 8001)
