import flask
import threading
import codecs
import shutil
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
from ModelV1 import db
from ModelV1 import User
from ModelV1 import Meeting
from ModelV1 import Rel_Meeting_User
from ModelV1 import Memo
from ModelV1 import Rel_Memo_User
from config import DevelopmentConfig
from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

import forms
import os

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
mail = Mail()
#Meeting
recipientsOfTheMeeting = {}
deletedUsers = []


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

@app.route('/viewDoc')
def viewDoc():

    return render_template('Employee/viewDoc.html')


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



_meetingMembers = {}

@app.route('/emitBill', methods=['GET','POST'])
def emitBill():
    obtainUserName()

    global _meetingMembers
    global deletedUsers

    idMeeting = request.args.get('idMeeting', None)
    issue    = request.args.get('issue', None)
    date = request.args.get('date', None)
    idMemberToRemove = request.args.get('idMemberToRemove',None)


    m = Meeting.query.all()
    rel = Rel_Meeting_User.query.all()
    val = session['idP']
    u = User.query.all()

    meetingMembers = {}
    temporaryList = []

    for r in rel:
        if r.idMeeting == int(idMeeting):
            for _u in u:
                if idMemberToRemove is None:
                    if _u.idPerson == r.idPerson:
                        temporaryList.append(_u.idPerson)
                        deletedUsers.clear()
                else:
                    if _u.idPerson == r.idPerson:
                        if not(_u.idPerson == int(idMemberToRemove)) and _u.idPerson not in deletedUsers:
                            temporaryList.append(_u.idPerson)
                        else:
                            deletedUsers.append(int(idMemberToRemove))

    #print(temporaryList)
    #print(idMemberToRemove)

    for i in temporaryList:
        aux = User.query.filter_by(idPerson = int(i)).first()
        print(aux.username)
        meetingMembers[int(i)] = aux

    _meetingMembers = meetingMembers
    print(_meetingMembers)
    
    if request.method == 'POST':
        flag1=True
        notfound=""
        cuerpo = select = request.form.get('body')
        rutas = []
        print(request.files.getlist("file[]"))
        target = os.path.join(APP_ROOT,'billFolder/')
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("file[]"):
            filename = file.filename
            print(filename)
            destination = "/".join([target,filename])
            rutas.append(filename)
            file.save(destination)

        for mem in _meetingMembers:
            aux_name =_meetingMembers[mem].username
            print("Nombre es "+ str(aux_name))
            aux_flag = False
            for r in rutas:
                name_file = r.split('_')[0]
                if name_file == aux_name:
                    aux_flag=True
            if(aux_flag == False):
                flag1=False
                notfound=aux_name
                break
        mensaje = ""
        if flag1 == True:
            flag = True
            mensaje = "Minuta registrada con exito!"
            for f in rutas:
                aux_text = "Holaaaaa"
                aux_text = aux_text.encode()
                h = SHA256.new(aux_text)
                priv_key = RSA.importKey(open("billFolder/"+f).read())
                singer = PKCS1_v1_5.new(priv_key)
                signature = singer.sign(h)

                hexify = codecs.getencoder ('hex')
                m = hexify(signature)[0]

                #aux_search = f.split('\\')[1]
                aux_search = f.split('_')[0]
                print(aux_search)
                user = db.session.query(User).filter(User.username == aux_search).one()
                print(user)
                uPublicKey = RSA.importKey(open(user.publicKey).read())
                verifier = PKCS1_v1_5.new(uPublicKey)

                if verifier.verify(h, signature) == False:
                    mensaje = "Error, la llave del siguiente usuario no es valida: " + str(aux_search)
                    flag = False
            
            print(idMeeting)
            print(_meetingMembers)
            print(cuerpo)

            if flag == True:
                #print("entramosssssssssss")
                aux_idmeet = idMeeting
                minuta = db.session.query(Meeting).filter(Meeting.idMeeting == idMeeting).one()
                minuta.path = cuerpo
                db.session.commit()    
        else:
            mensaje = "No se econtro una llave para "+notfound
        print(mensaje)

    return render_template('Employee/bill.html',issue = issue, date = date, members = meetingMembers.values(), idMeeting = idMeeting)

#@app.route('/removeMeetingParticipant', methods=['GET','POST'])
#def removeMeetingParticipant():
#    if request.method == 'POST':
#        print("prueba")
#    return redirect(url_for('emitBill'))



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

    flag = 1

    users = User.query.all()
    username = ""

    if request.method == 'POST':

        data = User.query.filter_by(username = request.form.get('searchField')).first()

        memorandumSubject = str(request.form.get('subject'))       .strip()
        memorandumType    = str(request.form.get('memorandumType')).strip()
        memorandumBody    = str(request.form.get('body'))          .strip()
        privateKey        =  request.files.getlist("file")

        #print(memorandumSubject)
        #print(memorandumType)
        #print(memorandumBody)
        #print(privateKey)

        filename = ""
        if memorandumType is not None and len(memorandumSubject) > 0 and len(memorandumBody) > 0 and privateKey is not None and not data:
            if privateKey is not None:
                target = os.path.join(APP_ROOT,'temporaryFolder/')
                if not os.path.isdir(target):
                    os.mkdir(target)
                for file in request.files.getlist("file"):
                    filename = file.filename
                    destination = "/".join([target,filename])
                    file.save(destination)
            try:
                memorandumType = memorandumType.split("=")[1]
            except:
                pass

            userKey = ""

            fileName = 'temporaryFolder/'+ filename

  #          file = open(fileName,'r')

 #           userKey = str(file.read())
#            file.close()
            aux_memo = memorandumBody
            memorandumBody = memorandumBody.encode()

            h = SHA256.new(memorandumBody)

            priv_key = RSA.importKey(open(fileName).read())
            singer = PKCS1_v1_5.new(priv_key)
            signature = singer.sign(h)

            hexify = codecs.getencoder ('hex')
            m = hexify(signature)[0]

            user = db.session.query(User).filter(User.position == 'CEO').one()
            #file = open(user.publicKey, 'r')
            ceoPublicKey = RSA.importKey(open(user.publicKey).read())
            #file.close()

            verifier = PKCS1_v1_5.new(ceoPublicKey)

            if verifier.verify(h, signature):
                print ("The signature is authentic.")
                flag = 2
                #new_memo = Memo(memorandumSubject,memorandumType,1,memorandumBody)
                # # db.session.add(new_memo)
                # db.session.commit()
                usuarios = User.query.all()
                if memorandumType is not "1":#
                    new_memo = Memo(memorandumSubject,memorandumType,1,'nada')
                    db.session.add(new_memo)
                    db.session.commit()
                    records = Memo.query.all()
                    lastMemo = -1
                    for r in records:
                        lastMemo = r.idMemo
                    print(lastMemo)
                    print(recipientsOfTheMemorandum)
                    print(usuarios)
                    for k in recipientsOfTheMemorandum:
                        for u in usuarios:
                            if k == u.idPerson:
                                auxM = memorandumBody

                                fileName = u.publicKey
                                print(fileName)
                                aux_public_key = RSA.importKey(open(fileName).read())

                                aux_cipher = PKCS1_OAEP.new(aux_public_key)
                                encrypted_message = aux_cipher.encrypt(auxM)

                                aux_hexify = codecs.getencoder('hex')
                                aux_m = hexify(encrypted_message)[0]

                                encrypted_message = aux_m.decode()
                                relation = Rel_Memo_User(k,lastMemo,encrypted_message)
                                db.session.add(relation)
                                db.session.commit()
                            else:
                                print(k)
                else:
                    new_memo = Memo(memorandumSubject,memorandumType,1,aux_memo)
                    db.session.add(new_memo)
                    db.session.commit()

            else:
                print ("The signature is not authentic.")
                flag = 3

        if data:
            if data.idPerson not in recipientsOfTheMemorandum.keys():
                recipientsOfTheMemorandum[data.idPerson] = data

    return render_template('CEO/emitMemorandum.html', users = users, dictionary = recipientsOfTheMemorandum, flag = flag, Mtype = Mtype)


@app.route('/rhdashboard')
def showRHDashBoard():
    mtngs = Meeting.query.all()
    rel_mtngs = Rel_Meeting_User.query.all()
    memos = Memo.query.all()
    rel_memo = Rel_Memo_User.query.all()
    return render_template('RH/RHDashboard.html',meetings = mtngs,rel_m_u = rel_mtngs,memo = memos,rel_memo = rel_memo)

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
            target = os.path.join(APP_ROOT,'privateKeys/')
            if not os.path.isdir(target):
                os.mkdir(target)

            key = RSA.generate(1024)
            privateKey = key.exportKey()
            publicKey  = key.publickey().exportKey()

            userName = str(user.username)

            fileName_prk = 'privateKeys/'+userName+"_privateKey.txt"
            fileName_puk = 'publicKeys/'+userName+"_publicKey.txt"

            file = open(fileName_prk,'wb')
            file.write(privateKey)

            file.close()

            _file = open(fileName_puk, 'wb')
            _file.write(publicKey)

            print(publicKey)

            _file.close()

            _user = db.session.query(User).filter(User.idPerson == id).one()
            _user.publicKey = fileName_puk
            db.session.commit()

            return send_file(fileName_prk, as_attachment=True)


    return render_template('RH/generatekeys.html', users = users)
@app.after_request
def after_request_callback(response):
    try:
        shutil.rmtree('privateKeys')
    except:
        pass
    return response

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

@app.route('/publicMemo', methods = ['GET','POST'])
def publicMemo():
    obtainUserName()
    getIdMemo = request.args.get('idM',None)
    mensaje = ""
    titulo = ""
    if request.method == 'GET':
        memos = Memo.query.all()
        for m in memos:
            if m.idMemo == int(getIdMemo):
                titulo = m.title
                mensaje = m.content

    return render_template('Employee/publicMemo.html',contenido=mensaje,issue = titulo)

@app.route('/showBill', methods = ['GET','POST'])
def showBill():
    obtainUserName()
    getIdMeet = request.args.get('idMeet',None)
    mensaje = ""
    titulo = ""
    date = ""
    if request.method == 'GET':
        meetings = Meeting.query.all()
        for m in meetings:
            if m.idMeeting == int(getIdMeet):
                mensaje = m.path
                titulo = m.issue
                date = str(m.date)

    return render_template('Employee/showBill.html',contenido=mensaje,issue=titulo,fecha=date)

@app.route('/addKey', methods = ['GET','POST'])
def addKey():
    fileNames = []
    obtainUserName()
    getIdMemo = request.args.get('idM',None)
    finalMessage = ""
    print(request.method)
    if request.method == 'POST':
        print("holaaaaa")
        privateKey        =  request.files.getlist("file")
        print(privateKey)
        if privateKey is not None:
            target = os.path.join(APP_ROOT,'temporaryFolder/')
            if not os.path.isdir(target):
                os.mkdir(target)
            for file in request.files.getlist("file"):
                filename = file.filename
                fileNames.append(filename)
                destination = "/".join([target,filename])
                print(destination)
                file.save(destination)
        try:
            memorandumType = memorandumType.split("=")[1]
        except:
            pass

        memorandumBody = "Holaquetal"
        memorandumBody = memorandumBody.encode()
        h = SHA256.new(memorandumBody)

        priv_key = RSA.importKey(open("temporaryFolder/"+fileNames[0]).read())
        singer = PKCS1_v1_5.new(priv_key)
        signature = singer.sign(h)

        hexify = codecs.getencoder ('hex')
        m = hexify(signature)[0]

        user = db.session.query(User).filter(User.idPerson == int(session['idP'])).one()
        print("ensenamos user")
        print(user)
        #file = open(user.publicKey, 'r')
        userPublicKey = RSA.importKey(open(user.publicKey).read())
        #file.close()

        verifier = PKCS1_v1_5.new(userPublicKey)

        finalMessage = "Error: Llave no valida"

        if verifier.verify(h, signature):
            getrelmemo = Rel_Memo_User.query.all()
            usuarios = User.query.all()
            print(getIdMemo)
            print(session['idP'])
            aux_idP = int(session['idP'])
            for aux_m in getrelmemo:
                print("Nueva")
                print(aux_m.idMemo)
                print(getIdMemo)
                print(aux_m.idMemo == int(getIdMemo))
                if aux_m.idMemo == int(getIdMemo):
                    if aux_m.idPerson == aux_idP:
                        mensaje = aux_m.cMessage

                        mensaje = mensaje.encode()
                        aux_hex = codecs.getdecoder('hex')
                        mensaje = aux_hex(mensaje)[0]
                        print("temporaryFolder/"+fileNames[0])
                        fileName = "temporaryFolder/"+fileNames[0]
                        private_key = RSA.importKey(open(fileName).read())
                        ciphered = PKCS1_OAEP.new(private_key)
                        finalMessage = str(ciphered.decrypt(mensaje))
                        finalMessage = finalMessage[2:-1]
                    else:
                        print("caca")
                else:
                    print("caca1")

    return render_template('Employee/addKey.html',printMessage=finalMessage)

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


@app.route('/removeUserM')
def removeUserM():
    id = request.args.get('id',None)
    del _meetingMembers[int(id)]
    issue = request.args.get('issue',None)
    date  = request.args.get('date',None)
    idMeeting = request.args.get('idMeeting',None)

    return redirect(url_for('emitBill',idMeeting = int(idMeeting), issue = issue, date = date, idMemberToRemove = id))


if __name__ == '__main__':
    db.init_app(app)
    mail.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port = 8001)
