from datetime import datetime
from webApp import db


# creating the admin table
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    prof_img = db.Column(db.String(20), nullable=False,
                         default='default.jpg')
    admin = db.Column(db.Boolean)
    doc = db.relationship('Documents', cascade='all,delete',
                          backref='admin_author', lazy=True)


# creating table for admin everyone section
class Documents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doc_file = db.Column('Document File', db.String(80), nullable=False,
                         default='No file Present')
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    admin_id = db.Column(db.String(50), db.ForeignKey('admin.public_id'),
                         nullable=False)


# creating the resident table
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    prof_img = db.Column(db.String(20), nullable=False,
                         default='default.jpg')
    admin = db.Column(db.Boolean)
    posts = db.relationship('Post', cascade='all,delete', backref='author',
                            lazy=True)
    requests = db.relationship('Requestuser', cascade='all,delete',
                               backref='author', lazy=True)
    repairs = db.relationship('Repairuser', cascade='all,delete',
                              backref='author', lazy=True)
    nights = db.relationship('Nightuser', cascade='all,delete',
                             backref='author', lazy=True)
    leaves = db.relationship('Leaveuser', cascade='all,delete',
                             backref='author', lazy=True)


# Post table for the resident uploaded post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_img = db.Column(db.String(20), nullable=False)
    caption = db.Column('Image Caption', db.Text, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    user_id = db.Column(db.String(50), db.ForeignKey('users.public_id'),
                        nullable=False)
    com = db.relationship('Comments', cascade='all,delete', backref='posted',
                          lazy=True)
    lk = db.relationship('Likemeter', cascade='all,delete', backref='posted',
                         lazy=True)


# comment table for the post of the particular resident
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comm = db.Column('Post Comments', db.Text, nullable=False)
    Commentor = db.Column(db.String(20), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


class Likemeter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    like_meter = db.Column('Post Likes', db.Boolean, nullable=False,
                           default=False)
    liker = db.Column(db.String(70), nullable=False)
    like_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


# Request Service table for the post of the particular resident
class Requestuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.String(10), unique=True, nullable=False)
    req_name = db.Column('Request Name', db.String(100), nullable=False)
    req = db.Column('Request', db.Text, nullable=False)
    status = db.Column('Approved/Pending', db.Boolean)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    req_id = db.Column(db.Integer, db.ForeignKey('users.public_id'),
                       nullable=False)


# Repair Service table for the post of the particular resident
class Repairuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repair_id = db.Column(db.String(10), unique=True, nullable=False)
    rep_name = db.Column('Repair Name', db.String(100), nullable=False)
    rep = db.Column('Repair', db.Text, nullable=False)
    status = db.Column('Approved/Pending', db.Boolean)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    rep_id = db.Column(db.Integer, db.ForeignKey('users.public_id'),
                       nullable=False)


# Night Out Application table for the post of the particular resident
class Nightuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    night_out_id = db.Column(db.String(10), unique=True, nullable=False)
    n_out_name = db.Column('Night Out Application Title', db.String(100),
                           nullable=False)
    n_out = db.Column('Night Out Application', db.Text, nullable=False)
    status = db.Column('Approved/Pending', db.Boolean)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    n_id = db.Column(db.Integer, db.ForeignKey('users.public_id'),
                     nullable=False)


# Leave Application table for the post of the particular resident
class Leaveuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.String(10), unique=True, nullable=False)
    lev_name = db.Column('Leave Aplication Title', db.String(100),
                         nullable=False)
    lev = db.Column('Leave Aplication', db.Text, nullable=False)
    status = db.Column('Approved/Pending', db.Boolean)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    lev_id = db.Column(db.Integer, db.ForeignKey('users.public_id'),
                       nullable=False)


# creating table for the cab services
class CabService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cab_id = db.Column(db.String(20), unique=True)
    name = db.Column('Cab Service Name', db.String(50), nullable=False)
    descp = db.Column('Description', db.Text, nullable=False)
    contact = db.Column('Contact Number', db.String(15), nullable=False)
    prof_img = db.Column(db.String(20), nullable=False,
                         default='default.jpg')


# creating table for the cab services
class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restraunt_id = db.Column(db.String(20), unique=True)
    name = db.Column('Restraunt Name', db.String(50), nullable=False)
    descp = db.Column('Description', db.Text, nullable=False)
    contact = db.Column('Contact Number', db.String(15), nullable=False)
    prof_img = db.Column(db.String(20), nullable=False,
                         default='default.jpg')
    menus = db.relationship('Menu', cascade='all,delete', backref='restraunt',
                            lazy=True)


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_item = db.Column('Menu Items', db.String(100), nullable=False)
    item_type = db.Column('Type', db.Boolean, nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.restraunt_id'),
                        nullable=False)
