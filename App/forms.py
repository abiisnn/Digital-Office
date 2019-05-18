from wtforms import Form
from wtforms import StringField, TextField
from wtforms.widgets import PasswordInput
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms import SelectField
from ModelV1 import db
from ModelV1 import User



def loginCheck(form,field):
    userName = str(field.data)
    user = db.session.query(User).filter(User.username == userName).first()
    if user is not None and user.status<1:
        raise validators.ValidationError('Your request has not yet been approved')
    if user is None:
        raise validators.ValidationError("The user isn't registered")

def registerCheck(form,field):
    userName = str(field.data)
    user = db.session.query(User).filter(User.username == userName).first()
    if user is not None:
        raise validators.ValidationError("The user is already registered")

class loginForm(Form):
    userName = StringField('Username',
        [
        validators.required(message = "The username is required"),
        validators.length(min = 4, max = 25, message = 'The lenght of the username is invalid'),
        loginCheck
        ])
    password = StringField('Password',
        [
        validators.required(message = 'The password is required'),
        validators.length(min = 8, max=25, message = 'The lenght of the password is invalid')
        ],widget=PasswordInput(hide_value=False))

class registerForm(Form):

    UserName = StringField('Username',
        [validators.required(message = "The username is required"),
         validators.length(min = 4, max = 25, message = 'The lenght of the username is invalid'),
         registerCheck
        ])

    Name = StringField('Name',
        [validators.required(message = "The name is required"),
         validators.length(min = 1, max = 25, message = 'The lenght of the name is invalid')
        ])

    LastName = StringField('Last Name',
        [validators.required(message = "The lastname is required"),
         validators.length(min = 1, max = 25, message = 'The lenght of the lastname is invalid')
        ])

    Email = EmailField('Email',
        [validators.Required(message = ' The email is requiered'),
         validators.Email(message = 'The email is invalid'),
         validators.length(min = 4, max = 50, message = 'The length of the email is invalid')
        ])

    Password = StringField('Password',
        [validators.Required(message='The password is required'),
         validators.length(min = 8, max=25, message = 'The lenght of the password is invalid')
        ], widget = PasswordInput(hide_value = False))

    Repeat_Password = StringField('Repeat Password',
        [validators.Required(message='The password is required'),
         validators.length(min = 8, max=25, message = 'The lenght of the password is invalid')
        ], widget = PasswordInput(hide_value = False))

    #    userName    = field.data
    #    userRequest        = UserRequest.query.filter_by(username = userName).first()
    #    user = User.query.filter_by(username = userName).first()
    #    if userRequest is not None or user is not None:
    #        raise validators.ValidationError('The username is already registered')
