from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField   
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from cms.models import Professor,Course

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired('Data required'),Email('email required')])
    password=PasswordField('Password',validators=[DataRequired('Data required')])
    submit=SubmitField('Login')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired('Data required')])
    email=StringField('Email',validators=[DataRequired('Data required'),Email('email required')])
    password=PasswordField('Password',validators=[DataRequired('Data required'),
    EqualTo('pass_confirm',message="Passwords must match!")])
    pass_confirm=PasswordField('Confirm Password',validators=[DataRequired('Data required')])
    branch = SelectField('Branch', validators=[DataRequired('Data required')],
                                            choices=[('CSE',"Computer Science"),('EE','Electrical'),('ME','Mechanical'),('CE','Civil')])
    submit=SubmitField('Regiss  ster')
    def validate_email(self,field):
        if Professor.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already')
    

class UpdateProfForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired('Data required'),Email('email required')])
    submit=SubmitField('Update')
    def check_email(self,field):
        if Professor.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already')
    
class addCourseForm(FlaskForm):
    name = StringField('Course Title', validators=[DataRequired('Data required')])
    course_code = StringField('Course code', validators=[DataRequired('Data required')])
    details = StringField('Course Details', validators=[DataRequired('Data required')])
    submit = SubmitField('Add Course')
    def validate_course_code(self,field):
        if Course.query.filter_by(course_code=field.data).first():
            raise ValidationError('Course code has already been registered')
