from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import  generate_password_hash, check_password_hash

db = SQLAlchemy()

friends = db.Table('friends',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)
requests = db.Table('requests',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('request_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)
sentrequests = db.Table('sentrequests',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('request_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

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
    friends = db.relationship('User', secondary=friends,
                              primaryjoin=(friends.c.user_id == id),
                              secondaryjoin=(friends.c.friend_id == id),
                              backref=db.backref('friend_of', lazy='dynamic'), lazy='dynamic')
    
    requests = db.relationship('User', secondary=requests,
                              primaryjoin=(requests.c.user_id == id),
                              secondaryjoin=(requests.c.request_id == id),
                              backref=db.backref('request_of', lazy='dynamic'), lazy='dynamic')
    sentrequests = db.relationship('User', secondary=sentrequests,
                              primaryjoin=(sentrequests.c.user_id == id),
                              secondaryjoin=(sentrequests.c.request_id == id),
                              backref=db.backref('sentrequest_of', lazy='dynamic'), lazy='dynamic')

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

