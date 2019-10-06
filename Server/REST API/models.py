import flask_sqlalchemy as SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
import json

from rest import db
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
