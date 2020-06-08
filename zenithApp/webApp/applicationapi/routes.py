import random
import string
from flask import Blueprint, jsonify, request, make_response
from webApp import db
from webApp.models import Users, Nightuser, Leaveuser
from webApp.utils import login_required

permission = Blueprint('Permission', __name__)


# get all the night out application
@permission.route('/application/night_out', methods=['GET'])
@login_required
def get_all_night(current_user):

    if not current_user.admin:
        return make_response('Not Permitted', 401)

    page = request.args.get('page', 1, type=int)
    nights = Nightuser.query.order_by(Nightuser.date_posted.desc())\
        .paginate(page=page, per_page=10)

    output = []

    for night in nights.items:
        output_data = {}
        output_data['night_id'] = night.night_out_id
        output_data['night_appli_name'] = night.n_out_name
        output_data['n_out'] = night.n_out
        output_data['approval'] = night.status
        output_data['date_posted'] = night.date_posted
        user = Users.query.filter_by(public_id=night.n_id).first()
        output_data['name'] = user.name
        output.append(output_data)

    return jsonify({'All Night Out Application': output})


# get all the leave application
@permission.route('/application/leave', methods=['GET'])
@login_required
def get_all_leave(current_user):

    if not current_user.admin:
        return make_response('Not Permitted', 401)

    page = request.args.get('page', 1, type=int)
    leaves = Leaveuser.query.order_by(Leaveuser.date_posted.desc())\
        .paginate(page=page, per_page=10)

    output = []

    for leave in leaves.items:
        output_data = {}
        output_data['leave_id'] = leave.application_id
        output_data['leave_name'] = leave.lev_name
        output_data['leave'] = leave.lev
        output_data['approval'] = leave.status
        output_data['date_posted'] = leave.date_posted
        user = Users.query.filter_by(public_id=leave.lev_id).first()
        output_data['name'] = user.name
        output.append(output_data)

    return jsonify({'All Leave Application': output})


# get specific the night out application
@permission.route('/application/night_out/user', methods=['GET'])
@login_required
def get_night(current_user):

    if not current_user.admin:

        page = request.args.get('page', 1, type=int)
        user = Users.query.filter_by(public_id=current_user.public_id)\
            .first()
        nights = Nightuser.query.order_by(Nightuser.date_posted.desc())\
            .filter_by(author=user)\
            .paginate(page=page, per_page=10)

        output = []

        for night in nights.items:
            output_data = {}
            output_data['night_id'] = night.night_out_id
            output_data['night_appli_name'] = night.n_out_name
            output_data['n_out'] = night.n_out
            output_data['approval'] = night.status
            output_data['date_posted'] = night.date_posted
            output_data['name'] = user.name
            output.append(output_data)

        return jsonify({'All Night Out Application by User': output})

    if current_user.admin:
        if request.args:
            data = request.args.get('public_id')

            page = request.args.get('page', 1, type=int)
            user = Users.query.filter_by(public_id=data).first()
            nights = Nightuser.query.order_by(Nightuser.date_posted.desc())\
                .filter_by(author=user)\
                .paginate(page=page, per_page=10)

            output = []

            for night in nights.items:
                output_data = {}
                output_data['night_id'] = night.night_out_id
                output_data['night_appli_name'] = night.n_out_name
                output_data['n_out'] = night.n_out
                output_data['approval'] = night.status
                output_data['date_posted'] = night.date_posted
                output_data['name'] = user.name
                output.append(output_data)

            return jsonify({'All Night Out Application by User': output})

    return make_response('You cannot access the records', 401)


# get specific the leave application
@permission.route('/application/leave/user', methods=['GET'])
@login_required
def get_leave(current_user):

    if not current_user.admin:

        page = request.args.get('page', 1, type=int)
        user = Users.query.filter_by(public_id=current_user.public_id)\
            .first()
        leaves = Leaveuser.query.order_by(Leaveuser.date_posted.desc())\
            .filter_by(author=user)\
            .paginate(page=page, per_page=10)

        output = []

        for leave in leaves.items:
            output_data = {}
            output_data['leave_id'] = leave.application_id
            output_data['leave_name'] = leave.lev_name
            output_data['leave'] = leave.lev
            output_data['approval'] = leave.status
            output_data['date_posted'] = leave.date_posted
            output_data['name'] = user.name
            output.append(output_data)

        return jsonify({'All Leave Application by User': output})

    if current_user.admin:
        if request.args:
            data = request.args.get('public_id')

            page = request.args.get('page', 1, type=int)
            user = Users.query.filter_by(public_id=data).first()
            leaves = Leaveuser.query.order_by(Leaveuser.date_posted.desc())\
                .filter_by(author=user)\
                .paginate(page=page, per_page=10)

            output = []

            for leave in leaves.items:
                output_data = {}
                output_data['leave_id'] = leave.application_id
                output_data['leave_name'] = leave.lev_name
                output_data['leave'] = leave.lev
                output_data['approval'] = leave.status
                output_data['date_posted'] = leave.date_posted
                output_data['name'] = user.name
                output.append(output_data)

            return jsonify({'All Leave Application by User': output})

    return make_response('You cannot access the records', 401)


# post specific the night out application
@permission.route('/application/night_out/user/new', methods=['POST'])
@login_required
def post_night(current_user):

    if not current_user.admin:

        name = request.form['night_out_name']
        info = request.form['night_out_info']

        alphabet = string.ascii_letters + string.digits
        night_out_id = ''.join(random.choice(alphabet) for i in range(7))

        user = Users.query.filter_by(public_id=current_user.public_id)\
            .first()
        night = Nightuser(night_out_id=night_out_id,
                          n_out_name=name,
                          n_out=info,
                          status=False,
                          author=user)

        db.session.add(night)
        db.session.commit()

        return jsonify({'msg': 'Night out aplication Sent Successfully!!'})

    return make_response('Only Resident users can submit a application', 401)


# post specific the leave application
@permission.route('/application/leave/user/new', methods=['POST'])
@login_required
def post_leave(current_user):

    if not current_user.admin:

        name = request.form['leave_name']
        info = request.form['leave_info']

        alphabet = string.ascii_letters + string.digits
        application_id = ''.join(random.choice(alphabet) for i in range(7))

        user = Users.query.filter_by(public_id=current_user.public_id)\
            .first()
        leave = Leaveuser(application_id=application_id,
                          lev_name=name,
                          lev=info,
                          status=False,
                          author=user)

        db.session.add(leave)
        db.session.commit()

        return jsonify({'msg': 'Leave aplication Sent Successfully!!'})

    return make_response('Only Resident users can submit a application', 401)


# permit specific the night out application
@permission.route('/application/night_out/update', methods=['PUT'])
@login_required
def permit_night(current_user):

    if not current_user.admin:
        data = request.get_json()
        night = Nightuser.query.filter_by(night_out_id=data['night_id'])\
            .first()

        night.n_out_name = data['night_name']
        night.n_out = data['night_info']

        db.session.commit()

        return({'msg': 'updated successfully!!'})

    if current_user.admin:
        if request.args:
            data = request.args
            night = Nightuser.query\
                .filter_by(night_out_id=data['night_id'])\
                .first()
            if data['status'] == '1':
                night.status = True
            elif data['status'] == '0':
                night.status = False

            db.session.commit()
            return({'night out application': night.n_out_name,
                    'status': night.status})

        return make_response('No arguments given', 401)

    return make_response('Not allowed any permission', 401)


# permit specific the leave application
@permission.route('/application/leave/update', methods=['PUT'])
@login_required
def permit_leave(current_user):

    if not current_user.admin:
        data = request.get_json()
        leave = Leaveuser.query\
            .filter_by(application_id=data['leave_id'])\
            .first()

        leave.lev_name = data['leave_name']
        leave.lev = data['leave_info']

        db.session.commit()

        return({'msg': 'updated successfully!!'})

    if current_user.admin:
        if request.args:
            data = request.args
            leave = Leaveuser.query\
                .filter_by(application_id=data['leave_id'])\
                .first()
            if data['status'] == '1':
                leave.status = True
            elif data['status'] == '0':
                leave.status = False

            db.session.commit()
            return({'leave out application': leave.lev_name,
                    'status': leave.status})

        return make_response('No arguments given', 401)

    return make_response('Not allowed any permission', 401)


# delete specific the night out application
@permission.route('/application/night_out/remove', methods=['DELETE'])
@login_required
def delete_night(current_user):

    if request.args:
        data = request.args.get('night_id')
        night = Nightuser.query.filter_by(night_out_id=data).first()

        db.session.delete(night)
        db.session.commit()

        return({'msg': 'Deleted Successfully!!'})

    return make_response('No arguments Given!!')


# delete specific the leave application
@permission.route('/application/leave/remove', methods=['DELETE'])
@login_required
def delete_leave(current_user):

    if request.args:
        data = request.args.get('leave_id')
        leave = Leaveuser.query.filter_by(application_id=data).first()

        db.session.delete(leave)
        db.session.commit()

        return({'msg': 'Deleted Successfully!!'})

    return make_response('No arguments Given!!')
