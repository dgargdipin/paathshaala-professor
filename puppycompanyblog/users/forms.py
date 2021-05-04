from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from puppycompanyblog.models import User

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired('Data required'),Email('email required')])
    password=PasswordField('Password',validators=[DataRequired('Data required')])
    submit=SubmitField('Login')

class RegistrationForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired('Data required'),Email('email required')])
    username=StringField('UserName',validators=[DataRequired('Data required')])
    password=PasswordField('Password',validators=[DataRequired('Data required'),
    EqualTo('pass_confirm',message="Passwords must match!")])
    pass_confirm=PasswordField('Confirm Password',validators=[DataRequired('Data required')])
    submit=SubmitField('Register')
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already')
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Your username has been registered already')

class UpdateUserForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired('Data required'),Email('email required')])
    username=StringField('UserName',validators=[DataRequired('Data required')])
    picture=FileField('Update Profile picture',validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Update')
    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already')
    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Your email has been registered already') 
    