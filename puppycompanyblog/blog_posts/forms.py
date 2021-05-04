from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

# from flask_login import current_user
# from puppycompanyblog.models import User


class BlogPostForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    text=TextAreaField('Text',validators=[DataRequired()])
    submit=SubmitField('Post')
