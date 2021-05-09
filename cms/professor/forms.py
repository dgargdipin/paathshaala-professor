from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField,SelectMultipleField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from cms.models import Professor,Course,Branch

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
    choices=[(branch.id,branch.name) for branch in Branch.query.all()]
    branch = SelectField('Branch', validators=[DataRequired('Data required')],
                                            choices=choices)
    submit=SubmitField('Register')
    def validate_email(self,field):
        if Professor.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already')
    

class UpdateProfForm(FlaskForm):
    email=StringField('Email',validators=[Email('email required')])
    password = StringField('Password')
    submit = SubmitField('Update')
    submit=SubmitField('Update')

    def validate_email(self, field):
        if Professor.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already')
    
class addCourseForm(FlaskForm):
    name = StringField('Course Title', validators=[DataRequired('Data required')])
    course_code = StringField('Course code', validators=[DataRequired('Data required')])
    choices=[(int(branch.id),branch.name) for branch in Branch.query.all()]
    print(choices)
    available_for=SelectMultipleField('Branches available for',validators=[DataRequired('Data required')],choices=choices,coerce=int)
    details = StringField('Course Details', validators=[DataRequired('Data required')])

    submit = SubmitField('Add Course')
    def validate_course_code(self,field):
        if Course.query.filter_by(course_code=field.data).first():
            raise ValidationError('Course code has already been registered')
