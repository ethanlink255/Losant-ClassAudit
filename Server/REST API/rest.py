from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required, login_manager
import flask_sqlalchemy as SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, send, emit
import json

#app configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "" #will come from pickle later
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret_holder" #TBD Change before transition to deployment
db = SQLAlchemy.SQLAlchemy(app)

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


#login configuration
login = LoginManager()
login.login_view = 'login'
login.init_app(app)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


import routes

if __name__ == '__main__':
    db.init_app(app)
    app.run()

