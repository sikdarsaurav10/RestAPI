import os
import secrets
from flask import request, jsonify, make_response
from webApp import app
from webApp.models import Admin, Users
from functools import wraps
import jwt


# decorator function to have all priviledges to admin
# taking in a token passed along with the login header
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # token name is x-access-header
        # passed when admin is logged in
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                current_user = Admin.query.filter_by(public_id=data['public_id'])\
                    .first()
            except Exception:
                return jsonify({'message': 'Token not valid!!'}), 401

        # token name is x-denied-header
        # passed when user is logged in
        if 'x-denied-token' in request.headers:
            token = request.headers['x-denied-token']

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                current_user = Users.query.filter_by(public_id=data['public_id'])\
                    .first()
            except Exception:
                return jsonify({'message': 'Token not valid!!'}), 401

        if not token:
            return make_response('Token is missing!!', 401)

        return f(current_user, *args, **kwargs)

    return decorated


# function to convert and return the uploaded profile image
# only allowed file extension to be saved
# image file name changed so that saving is easy and ambiguity dosen't occur
def save_pic(prof_pic, c_user):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(prof_pic.filename)
    file_ext_allowed = [".jpg", ".png", ".jpeg"]
    if f_ext in file_ext_allowed:
        # if the user is an admin
        if not c_user.admin:
            pic_fn = random_hex + f_ext
            pic_path = os.path.join(app.root_path,
                                    'static/images/profile_pics/user',
                                    pic_fn)
            prof_pic.save(pic_path)
            return pic_fn
        # if the user is a resident
        pic_fn = random_hex + f_ext
        pic_path = os.path.join(app.root_path,
                                'static/images/profile_pics/admin',
                                pic_fn)
        prof_pic.save(pic_path)
        return pic_fn
    return "Not allowed"


def save_cab_pic(prof_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(prof_pic.filename)
    file_ext_allowed = [".jpg", ".png", ".jpeg"]
    if f_ext in file_ext_allowed:
        pic_fn = random_hex + f_ext
        pic_path = os.path.join(app.root_path,
                                'static/images/cab_service_img/',
                                pic_fn)
        prof_pic.save(pic_path)
        return pic_fn
    return "Not allowed"


def save_rest_pic(prof_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(prof_pic.filename)
    file_ext_allowed = [".jpg", ".png", ".jpeg"]
    if f_ext in file_ext_allowed:
        pic_fn = random_hex + f_ext
        pic_path = os.path.join(app.root_path,
                                'static/images/restraunt_service_img/',
                                pic_fn)
        prof_pic.save(pic_path)
        return pic_fn
    return "Not allowed"


def save_Doc_admin(document):
    f_name, f_ext = os.path.splitext(document.filename)
    file_ext_allowed = [".txt", ".pdf", ".docx", ".doc"]
    if f_ext in file_ext_allowed:
        doc_fn = f_name + f_ext
        doc_path = os.path.join(app.root_path,
                                'static/adminDocuments/',
                                doc_fn)
        document.save(doc_path)
        return doc_fn
    return "Not allowed"


def save_post(picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    file_ext_allowed = [".jpg", ".png", ".jpeg"]
    if f_ext in file_ext_allowed:
        pic_fn = random_hex + f_ext
        pic_path = os.path.join(app.root_path,
                                'static/images/posts/',
                                pic_fn)
        picture.save(pic_path)
        return pic_fn
    return "Not Uploaded"
