from flask import jsonify, request, make_response, url_for
from webApp import app, db
from webApp.models import Users, Admin, Documents
from webApp.utils import login_required, save_pic, save_Doc_admin
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime


# landing page after the login
# residents and admin land in different pages based on their roles
@app.route('/', methods=['GET'])
@login_required
def index(current_user):
    if not current_user.admin:
        return make_response('Welcome Resident')

    return make_response('Welcome Admin')


# get all the user details from the Resident table
# only admin is allowed to do that
@app.route('/user', methods=['GET'])
@login_required
def get_all_users(current_user):

    if not current_user.admin:
        return make_response('You are not permitted!!', 401)

    users = Users.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['name'] = user.name
        user_data['prof_image'] = user.prof_img
        output.append(user_data)

    return jsonify({'Users': output})


# get all the details of the admin users
@app.route('/user/admin', methods=['GET'])
@login_required
def get_all_admins(current_user):

    if not current_user.admin:
        return make_response('You are not permitted!!', 401)

    users = Admin.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['name'] = user.name
        user_data['prof_image'] = user.prof_img
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'Admins': output})


# create a new "ADMIN USER"
@app.route('/user/admin/new', methods=['POST'])
def create_admin():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = Admin(public_id=str(uuid.uuid4()),
                     username=data['username'],
                     password=hashed_password,
                     name=data['name'],
                     admin=True)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New admin user created'})


# create a new "RESIDENT USER"
# "CAN ONLY BE CREATED BY THE ADMIN"
@app.route('/user/new', methods=['POST'])
@login_required
def create_user(current_user):

    if not current_user.admin:
        return make_response('You are not permitted!!')

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = Users(public_id=str(uuid.uuid4()),
                     username=data['username'],
                     password=hashed_password,
                     name=data['name'],
                     admin=False)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created'})


# get details of a specific user
@app.route('/user/<public_id>', methods=['GET'])
@login_required
def get_user(current_user, public_id):

    if not current_user.admin:
        return make_response('You are not permitted!!', 401)

    user = Users.query.filter_by(public_id=public_id).first_or_404()

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['username'] = user.username
    user_data['password'] = user.password
    user_data['name'] = user.name
    user_data['prof_image'] = user.prof_img

    return jsonify({'User': user_data})


@app.route('/user/remove', methods=['DELETE'])
@login_required
def delete_user(current_user):

    if not current_user.admin:
        return make_response('You are not permitted!!')

    if request.args:
        data = request.args.get('public_id')

        user = Users.query.filter_by(public_id=data).first()

        if not user:
            return jsonify({'message': 'NO USER FOUND!!'})

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'USER DELETED!!'})

    return make_response('No arguments passed for record deletion!!', 401)


'''
token are being generated and passed,
into different headers to distinguish between admin and resident,
and also to keep the particular user(resident/user) logged in.
'''


# login for the admin, only CRUD priviledges provided to admin
# the token is passed into the x-access-header here
@app.route('/login/admin', methods=['POST'])
def sigin_admin():
    '''
    getting username and pasword from the http header
    header is passed with the username and the password
    '''
    auth = request.get_json()

    if not auth or not auth['username'] or not auth['password']:
        return make_response('Could not verify', 404, {
            'WWW-authenticate': 'Basic realm="Login Required!"'})

    user = Admin.query.filter_by(username=auth['username']).first()

    if not user:
        return make_response('Could not verify', 404, {
            'WWW-authenticate': 'Basic realm="Login Required!"'})

    if check_password_hash(user.password, auth['password']):
        token = jwt.encode(
            {'public_id': user.public_id,
             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'])

        return jsonify({'message': 'Login Successful!',
                        'token': token.decode('UTF-8')})

    return make_response('Could not verify', 404,
                         {'WWW-authenticate': 'Basic realm="Login Required!"'})


# login for the users
# the token is passed into the x-hidden-header here
@app.route('/login/user', methods=['POST'])
def sigin_user():
    '''
    getting username and pasword from the http header
    header is passed with the username and the password
    '''
    auth = request.get_json()

    if not auth or not auth['username'] or not auth['password']:
        return make_response('Could not verify', 404, {
            'WWW-authenticate': 'Basic realm="Login Required!"'})

    user = Users.query.filter_by(username=auth['username']).first()

    if not user:
        return make_response('Could not verify', 404, {
            'WWW-authenticate': 'Basic realm="Login Required!"'})

    if check_password_hash(user.password, auth['password']):
        token = jwt.encode(
            {'public_id': user.public_id,
             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'])

        return jsonify({'message': 'Login Successful!',
                        'token': token.decode('UTF-8')})

    return make_response('Could not verify', 404,
                         {'WWW-authenticate': 'Basic realm="Login Required!"'})


# to get the admin profile pic
@app.route('/user/admin/prof_pic', methods=['GET'])
@login_required
def get_admin_prof_pic(current_user):
    if not current_user.admin:
        return make_response('You are not permitted!!')

    image_file = url_for('static', filename='images/profile_pics/admin/' + current_user.prof_img)
    return jsonify({'admin_prof_img_url': image_file})


# to get the user profile pic
@app.route('/user/prof_pic', methods=['GET'])
@login_required
def get_user_prof_pic(current_user):
    if current_user.admin:
        return make_response('You are not permitted!!')

    image_file = url_for('static', filename='images/profile_pics/user/' + current_user.prof_img)
    return jsonify({'user_prof_img_url': image_file})


# to upload and save the admin profile pic
@app.route('/user/admin/prof_pic/upload', methods=['PUT'])
@login_required
def admin_prof_pic(current_user):
    if not current_user.admin:
        return make_response('Not Permitted', 401)

    file_name = request.files['file']
    file_t = save_pic(file_name, current_user)
    user = Admin.query.filter_by(public_id=current_user.public_id).first()
    user.prof_img = file_t

    db.session.commit()

    return jsonify({'file name': file_t})


# to upload and save the user profile pic by passing the public_id
# in the url so that admin can select and only he can do it
@app.route('/user/prof_pic/upload', methods=['PUT'])
@login_required
def user_prof_pic(current_user):
    if current_user.admin:
        return make_response('Not Permitted', 401)

    file_name = request.files['file']
    user = Users.query.filter_by(public_id=current_user.public_id).first()
    file_t = save_pic(file_name, user)
    user.prof_img = file_t

    db.session.commit()

    return jsonify({'file name': file_t})


# upload the documents for the admin everyone section
@app.route('/user/admin/everyone/upload', methods=['POST'])
@login_required
def admin_Doc_upload(current_user):
    if not current_user.admin:
        return make_response('Not Permitted', 401)

    file_name = request.files['Doc_file']
    file_t = save_Doc_admin(file_name)
    user = Admin.query.filter_by(public_id=current_user.public_id).first()

    doc = Documents(doc_file=file_t, admin_id=user.public_id)

    db.session.add(doc)
    db.session.commit()

    return jsonify({'file name': file_t})


# get the documents for the admin everyone section
@app.route('/user/admin/everyone', methods=['GET'])
@login_required
def get_admin_Doc(current_user):
    if not current_user.admin:
        return make_response('Not Permitted', 401)

    doc = Documents.query.filter_by(admin_author=current_user).all()

    output = []
    for item in doc:
        output_data = {}
        output_data['Document File'] = item.doc_file
        output.append(output_data)

    files = []
    for item in output:
        doc_files = url_for('static',
                            filename='adminDocuments/' + item['Document File'])
        files.append(doc_files)

    return jsonify({'file name': files})


# delete the documents for the admin everyone section
@app.route('/user/admin/everyone/remove', methods=['DELETE'])
@login_required
def remove_admin_Doc(current_user):
    if not current_user.admin:
        return make_response('Not Permitted', 401)

    if request.args:
        data = request.args.get('Doc')

        doc = Documents.query.filter_by(admin_id=current_user.public_id)\
            .filter_by(doc_file=data).first()

        if not doc:
            return jsonify({'message': 'NO DOCUMENT FOUND!!'})

        db.session.delete(doc)
        db.session.commit()

        return ({'message': 'Document Deleted'})

    return make_response('No document argument given', 401)
