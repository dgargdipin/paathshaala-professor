from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
app =Flask(__name__)
app.config['SECRET_KEY']='mysecret'
basedir=os.path.abspath(os.path.dirname(__file__))
print(basedir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, '..', 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
if os.getenv('testing')=='true':
    print("TESTING MODE")
    app.config['WTF_CSRF_ENABLED']=False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, '..', '..', 'data_test.sqlite')

db=SQLAlchemy(app)



login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'professors.login'
ALLOWED_EXT = ['pdf', 'jpg', 'jpeg', 'png']
import cms.models
import cms.branch_helper as branch_helper
db.create_all()
db.session.add_all(branch_helper.create_branch_array())
db.session.commit()

from cms.core.views import core
from cms.error_pages.handlers import error_pages
from cms.professor.views import professors
from cms.course.views import CourseBluerint
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(professors)
app.register_blueprint(CourseBluerint)
print("route path is, ", core.root_path )
