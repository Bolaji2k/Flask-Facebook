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
grouprequests = db.Table('grouprequests',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)
sender = db.Table('sender',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('chat_id', db.Integer, db.ForeignKey('chats.id'), primary_key=True)
)
members = db.Table('members',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True),
    db.Column('member_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)
groupchats = db.Table('groupchats',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True),
    db.Column('chat_id', db.Integer, db.ForeignKey('chats.id'), primary_key=True)
)
admin = db.Table('admin',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True),
    db.Column('admin_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)



class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    file_path = db.Column(db.String(100), nullable=True)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    gender = db.Column(db.String(7), default="Female")
    about = db.Column(db.Text, nullable=True)
    state = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)
    age = db.Column(db.SmallInteger)
    password_hash = db.Column(db.String(255))
    profile_img = db.Column(db.String(255), nullable=True)
    cover_img = db.Column(db.String(255), nullable=True)
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
    
    def length(self):
        num = 0
        for i in self.friends:
            num += 1
        return num

class Chat(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    sender = db.relationship('User', secondary=sender,
                              primaryjoin=(sender.c.user_id == User.id),
                              secondaryjoin=(sender.c.chat_id == id),
                              backref=db.backref('chat_of', lazy='dynamic'), lazy='dynamic')
    

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    members = db.relationship('User', secondary=members,
                              primaryjoin=(members.c.group_id == id),
                              secondaryjoin=(members.c.member_id == User.id),
                              backref=db.backref('member_of', lazy='dynamic'), lazy='dynamic')
    admin = db.relationship('User', secondary=admin,
                              primaryjoin=(admin.c.group_id == id),
                              secondaryjoin=(admin.c.admin_id == User.id),
                              backref=db.backref('admin_of', lazy='dynamic'), lazy='dynamic')
    groupchats = db.relationship('Chat', secondary=groupchats,
                              primaryjoin=(groupchats.c.group_id == id),
                              secondaryjoin=(groupchats.c.chat_id == Chat.id),
                              backref=db.backref('groupchats_of', lazy='dynamic'), lazy='dynamic')
    grouprequests = db.relationship('User', secondary=grouprequests,
                              primaryjoin=(grouprequests.c.group_id == id),
                              secondaryjoin=(grouprequests.c.user_id == User.id),
                              backref=db.backref('grouprequests_of', lazy='dynamic'), lazy='dynamic')

    def length(self):
        num = 0
        for i in self.members:
            num += 1
        return num


