from flask import Flask
from flask import request
from flask import render_template
from flask import make_response
from flask_material import Material
from flask import session
from flask_wtf import CSRFProtect
import forms

app = Flask(__name__)
app.secret_key = "1234"
csrf = CSRFProtect(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cookie')
def cookie():
    response = make_response(render_template('cookie.html'))
    response.set_cookie('custome_cookie', 'prueba')
    return response


@app.route('/login', methods = ['GET', 'POST'])
def showLoginForm():
    loginForm = forms.loginForm(request.form)

    if request.method == 'POST' and loginForm.validate():
        session['userName'] = loginForm.userName.data
        session['password'] = loginForm.password.data

    return render_template('dashboard.html', form = loginForm)

if __name__ == '__main__':
    app.run(debug = True, port = 8000)
