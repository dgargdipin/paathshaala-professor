from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager
from sqlalchemy.orm import session
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, '..', '..', 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db, render_as_batch=True)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'professors.login'

import cms.models
db.create_all()
from cms.branch_helper import create_branch_array
db.session.add_all(create_branch_array())
db.session.commit()
db.session.add(cms.models.User('Dipin','dgargdipin@gmail.com','dipin','2',1))
db.session.add(cms.models.Professor('Professor One','prof1@gmail.com','prof1','1'))
db.session.commit()
