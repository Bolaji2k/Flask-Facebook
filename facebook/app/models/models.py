from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import  generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    gender = db.Column(db.String(7), default="Female")
    about = db.Column(db.Text)
    address = db.Column(db.Text)
    age = db.Column(db.SmallInteger)
    password_hash = db.Column(db.String(255))

    def __repr__(self) -> str:
        return f'<User {self.email}>'
    
    @property 
    def password(self):
        raise AttributeError("Password is not a readable attribute")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
