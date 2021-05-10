from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, SelectMultipleField, TextAreaField, \
    BooleanField, IntegerField
from wtforms.fields.simple import MultipleFileField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateTimeLocalField
from flask_login import current_user
from cms.models import Professor, Course, Branch


class quizForm(FlaskForm):
    name = StringField('Quiz Name', validators=[DataRequired('Data required')])
    start_time = DateTimeLocalField('Start Time and Date:', validators=[DataRequired('Data required')],
                                    format='%Y-%m-%dT%H:%M')
    end_time = DateTimeLocalField('End Time and Date:', validators=[DataRequired('Data required')],
                                  format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Submit')


class addCourseNote(FlaskForm):
    # id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(100))
    # details = db.Column(db.String(100))
    # attachments=db.relationship('Attachment',backref='coursenote')
    # course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    # def __init__(self,title,details,course_id):
    #     self.title=title
    #     self.details=details
    #     self.course_id=course_id
    title = StringField('Note Title', validators=[DataRequired('Data required')])
    details = TextAreaField('Details', validators=[DataRequired('Data required')])
    attachments = MultipleFileField('Attachments')
    submit1 = SubmitField('Submit')


class assignmentForm(addCourseNote):
    title = StringField('Note Title', validators=[DataRequired('Data required')])
    details = TextAreaField('Details', validators=[DataRequired('Data required')])
    attachments = MultipleFileField('Attachments')
    deadline = DateTimeLocalField('Deadline for submission', validators=[DataRequired('Data required')],
                                  format='%Y-%m-%dT%H:%M')
    submit2 = SubmitField('Submit')


class questionForm(FlaskForm):
    question = StringField('Question ?', validators=[DataRequired('Data required')])
    is_multi_correct = BooleanField('Multi Correct Question ?')
    is_partial = BooleanField('Partial Marking ?')
    marks = IntegerField('Marks')
    option1 = StringField('Option 1', validators=[DataRequired('Data required')])
    option2 = StringField('Option 2', validators=[DataRequired('Data required')])
    option3 = StringField('Option 3', validators=[DataRequired('Data required')])
    option4 = StringField('Option 4', validators=[DataRequired('Data required')])

    ans = StringField('Enter answer options', validators=[DataRequired('Data required')])
    submit = SubmitField('Submit')


class postForm(FlaskForm):
    details = TextAreaField('Details', validators=[DataRequired('Data required')])
    attachments = MultipleFileField('Attachments')
    submit = SubmitField('Submit')