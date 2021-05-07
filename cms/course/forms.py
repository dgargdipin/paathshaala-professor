from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField,SelectMultipleField,TextAreaField
from wtforms.fields.simple import MultipleFileField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed
from wtforms.fields.html5 import DateTimeLocalField
from flask_login import current_user
from cms.models import Professor,Course,Branch

class addCourseNote(FlaskForm):
    # id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String())
    # details = db.Column(db.String())
    # attachments=db.relationship('Attachment',backref='coursenote')
    # course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    # def __init__(self,title,details,course_id):
    #     self.title=title
    #     self.details=details
    #     self.course_id=course_id
    title = StringField('Note Title', validators=[DataRequired('Data required')])
    details = TextAreaField('Details', validators=[DataRequired('Data required')])
    attachments=MultipleFileField('Attachments')
    submit1=SubmitField('Submit')
class assignmentForm(addCourseNote):
    title = StringField('Note Title', validators=[DataRequired('Data required')])
    details = TextAreaField('Details', validators=[DataRequired('Data required')])
    attachments=MultipleFileField('Attachments')
    deadline=DateTimeLocalField('Deadline for submission',validators=[DataRequired('Data required')],format='%Y-%m-%dT%H:%M')
    submit2=SubmitField('Submit')
