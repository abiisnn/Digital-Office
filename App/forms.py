from wtforms import Form
from wtforms import StringField, TextField
from wtforms.widgets import PasswordInput
from wtforms.fields.html5 import EmailField
from wtforms import validators

class loginForm(Form):

    userName = StringField('Username',
        [
        validators.required(message = "The username is required"),
        validators.length(min = 4, max = 25, message = 'The lenght of the username is invalid')
        ])
    password = StringField('Password',
        [
        validators.required(message = 'The password is required'),
        validators.length(min = 8, max=25, message = 'The lenght of the password is invalid')
        ],widget=PasswordInput(hide_value=False))

class registerForm(Form):

    Name = StringField('Name',
        [validators.required(message = "The username is required"),
         validators.length(min = 1, max = 25, message = 'The lenght of the username is invalid')
        ])

    LastName = StringField('Last Name',
        [validators.required(message = "The username is required"),
         validators.length(min = 1, max = 25, message = 'The lenght of the username is invalid')
        ])

    UserName = StringField('Username',
        [validators.required(message = "The username is required"),
         validators.length(min = 4, max = 25, message = 'The lenght of the username is invalid')
        ])

    Email = EmailField('Email',
        [validators.Required(message = ' The email is requiered'),
         validators.Email(message = 'The email is invalid'),
         validators.length(min = 4, max = 50, message = 'The length of the email is invalid')
        ])

    Employment = StringField('Employment',
        [validators.required(message = "The username is required"),
         validators.length(min = 4, max = 25, message = 'The lenght of the username is invalid')
        ])

    Office = StringField('Office',
        [validators.required(message = "The username is required"),
         validators.length(min = 4, max = 25, message = 'The lenght of the username is invalid')
        ])

    Password = StringField('Password',
        [validators.Required(message='The password is required'),
         validators.length(min = 8, max=25, message = 'The lenght of the password is invalid')
        ], widget = PasswordInput(hide_value = False))

    Repeat_Password = StringField('Repeat Password',
        [validators.Required(message='The password is required'),
         validators.length(min = 8, max=25, message = 'The lenght of the password is invalid')
        ], widget = PasswordInput(hide_value = False))
