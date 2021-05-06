from enum import unique
# from cms.core.views import index
from cms import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return Professor.query.get(user_id)


course_helper=db.Table('course_helper',
                        db.Column('user_id',db.Integer,db.ForeignKey('users.id')),
                        db.Column('course_id',db.Integer,db.ForeignKey('courses.id'))
                        )

class User(db.Model,UserMixin):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    password_hash=db.Column(db.String(128))
    year=db.Column(db.Integer())
    branch=db.Column(db.String())
    courses = db.relationship('Course', secondary=course_helper,
                              backref=db.backref('students'))
    def __init__(self,email,password,year,branch):
        self.email=email
        self.password_hash=generate_password_hash(password)
        self.year=year
        self.branch=branch

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


class Course(db.Model):
    __tablename__='courses'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String())
    details=db.Column(db.String())
    prof_id = db.Column(db.Integer, db.ForeignKey('professors.id'), nullable=False)
    course_code=db.Column(db.String(),unique=True)

    def __init__(self, name, course_code, details, prof_id):
        self.name=name
        self.course_code = course_code
        self.details=details
        self.prof_id=prof_id
    

class Professor(db.Model, UserMixin):
    __tablename__ = 'professors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String(64), unique=True, index=True)
    branch=db.Column(db.String())
    courses=db.relationship('Course',backref='professor',lazy=True)
    password_hash = db.Column(db.String(128))
    
    def __init__(self,name,email,password,branch):
        self.email = email
        self.name=name
        self.password_hash=generate_password_hash(password)
        self.branch=branch

    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
