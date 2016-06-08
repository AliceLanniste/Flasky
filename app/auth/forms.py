#coding:utf-8
from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField,ValidationError
from wtforms.validators import Required,Length,Email,Regexp
from ..models import User
#create loginForm
class LoginForm(Form):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    password=PasswordField('Password',validators=[Required()])
    remember_me=BooleanField('keep me login in')
    submit=SubmitField('Login In')
#create registerForm
class RegisterForm(Form):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    username=StringField('Username',validators=[Required(),Length(1,64),
                        Regexp('^[A-Za-z][A-Za-z0-9_]*$',0,
                               'username must have only letters,numbers and underscores')])
    password=PasswordField('Password',validators=[Required()])
    submit=SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('you have registered')
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username alreay in use')


