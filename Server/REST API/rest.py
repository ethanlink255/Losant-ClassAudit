from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required, login_manager
import flask_sqlalchemy as SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, send, emit
import json
from datetime import datetime

#app configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://hallways:_&?*2qkS$wKSQ%5GqT7PFA^-Yx%j!=@localhost/student_log" #will come from pickle later
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret_holder" #TBD Change before transition to deployment
db = SQLAlchemy.SQLAlchemy(app)

#region Models

#Helper table, no need for model
student_class = db.Table('student_classes',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('classes.id'), primary_key=True)

)
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String()) #hashed of course

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()
    def check_password(self, password_data):
        if check_password_hash(self.password, password_data):
            return True
        else:
            return False

class Classes(db.Model):
    __tablename__ = "classes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    teacher = db.Column(db.String(80))
    period = db.Column(db.Integer)
    student = db.relationship('Students', secondary=student_class, lazy='subquery',backref=db.backref('Classes', lazy=True))
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()
    

class Students(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    uuid = db.Column(db.String(10))
    classes = db.relationship('Classes', secondary=student_class, lazy='subquery',backref=db.backref('Students', lazy=True))

    def __init__(self, id, first_name, last_name, uuid):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.uuid = uuid

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
      
    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

class Students_out(db.Model):
    __tablename__ = "students_out"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id')) 
    time_out = db.Column(db.DateTime, default=datetime.utcnow)
    destination = db.Column(db.String(255))

    def __init__(self, student_id, class_id, destination):
        self.student_id = student_id
        self.class_id = class_id
        self.destination = destination

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

      
    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

class Log(db.Model):
    __tablename__ = "log"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id')) 
    a_time = db.Column(db.DateTime, default=datetime.utcnow)
    a_type = db.Column(db.String(255))
    destination = db.Column(db.String(255))

    def __init__(self, student_id, class_id, a_type, destination):
        self.student_id = student_id
        self.class_id = class_id
        self.a_type = a_type
        self.destination = destination

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

      
    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

class Dashboard(db.Model):
    __tablename__ = "dashboards"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    url = db.Column(db.Text)

    def __init__(self, description, url):
        self.description = description
        self.url = url
        

#endregion

#login configuration
login = LoginManager()
login.login_view = 'login'
login.init_app(app)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

from routes import *

if __name__ == '__main__':
    db.init_app(app)
    app.run(host='0.0.0.0')

