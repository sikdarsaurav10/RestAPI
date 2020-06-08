import random
import string
from flask import Blueprint, jsonify, request, make_response
from webApp import db
from webApp.models import Users, Repairuser, Requestuser
from webApp.utils import login_required

support = Blueprint('Support', __name__)


# get all the request
@support.route('/request', methods=['GET'])
@login_required
def get_all_request(current_user):

    if not current_user.admin:
        return make_response('Not Permitted', 401)

    page = request.args.get('page', 1, type=int)
    requests = Requestuser.query.order_by(Requestuser.date_posted.desc())\
        .paginate(page=page, per_page=10)

    output = []

    for requ in requests.items:
        output_data = {}
        output_data['req_id'] = requ.request_id
        output_data['req_name'] = requ.req_name
        output_data['req'] = requ.req
        output_data['approval'] = requ.status
        output_data['date_posted'] = requ.date_posted
        user = Users.query.filter_by(public_id=requ.req_id).first()
        output_data['name'] = user.name
        output.append(output_data)

    return jsonify({'All Requests': output})


# get all the repair
@support.route('/repair', methods=['GET'])
@login_required
def get_all_repair(current_user):

    if not current_user.admin:
        return make_response('Not Permitted', 401)

    page = request.args.get('page', 1, type=int)
    repairs = Repairuser.query.order_by(Repairuser.date_posted.desc())\
        .paginate(page=page, per_page=10)

    output = []

    for repair in repairs.items:
        output_data = {}
        output_data['rep_id'] = repair.repair_id
        output_data['rep_name'] = repair.rep_name
        output_data['rep'] = repair.rep
        output_data['approval'] = repair.status
        output_data['date_posted'] = repair.date_posted
        user = Users.query.filter_by(public_id=repair.rep_id).first()
        output_data['name'] = user.name
        output.append(output_data)

    return jsonify({'All Repairs': output})


# get specific the request made by user
@support.route('/request/user', methods=['GET'])
@login_required
def get_request(current_user):

    if not current_user.admin:

        page = request.args.get('page', 1, type=int)
        user = Users.query.filter_by(public_id=current_user.public_id).first()
        requests = Requestuser.query\
            .order_by(Requestuser.date_posted.desc())\
            .filter_by(author=user)\
            .paginate(page=page, per_page=10)

        output = []

        for requ in requests.items:
            output_data = {}
            output_data['req_id'] = requ.request_id
            output_data['req_name'] = requ.req_name
            output_data['req'] = requ.req
            output_data['approval'] = requ.status
            output_data['date_posted'] = requ.date_posted
            output_data['name'] = user.name
            output.append(output_data)

        return jsonify({'All Requests by User': output})

    if current_user.admin:

        if request.args:
            data = request.args.get('public_id')

            page = request.args.get('page', 1, type=int)
            user = Users.query.filter_by(public_id=data).first()
            requests = Requestuser.query\
                .order_by(Requestuser.date_posted.desc())\
                .filter_by(author=user)\
                .paginate(page=page, per_page=10)

            output = []

            for requ in requests.items:
                output_data = {}
                output_data['req_id'] = requ.request_id
                output_data['req_name'] = requ.req_name
                output_data['req'] = requ.req
                output_data['approval'] = requ.status
                output_data['date_posted'] = requ.date_posted
                output_data['name'] = user.name
                output.append(output_data)

            return jsonify({'All Requests by User': output})

        return make_response('No arguments given', 401)

    return make_response('You cannot access the records', 401)


# get specific the repair
@support.route('/repair/user', methods=['GET'])
@login_required
def get_repair(current_user):

    if not current_user.admin:

        page = request.args.get('page', 1, type=int)
        user = Users.query.filter_by(public_id=current_user.public_id).first()
        repairs = Repairuser.query.order_by(Repairuser.date_posted.desc())\
            .filter_by(author=user)\
            .paginate(page=page, per_page=10)

        output = []

        for repair in repairs.items:
            output_data = {}
            output_data['rep_id'] = repair.repair_id
            output_data['rep_name'] = repair.rep_name
            output_data['rep'] = repair.rep
            output_data['approval'] = repair.status
            output_data['date_posted'] = repair.date_posted
            output_data['name'] = user.name
            output.append(output_data)

        return jsonify({'All Repairs by user': output})

    if current_user.admin:

        if request.args:
            data = request.args.get('public_id')

            page = request.args.get('page', 1, type=int)
            user = Users.query.filter_by(public_id=data).first()
            repairs = Repairuser.query\
                .order_by(Repairuser.date_posted.desc())\
                .filter_by(author=user)\
                .paginate(page=page, per_page=10)

            output = []

            for repair in repairs.items:
                output_data = {}
                output_data['rep_id'] = repair.repair_id
                output_data['rep_name'] = repair.rep_name
                output_data['rep'] = repair.rep
                output_data['approval'] = repair.status
                output_data['date_posted'] = repair.date_posted
                output_data['name'] = user.name
                output.append(output_data)

            return jsonify({'All Repairs by user': output})

        return make_response('No arguments given', 401)

    return make_response('You cannot access the records', 401)


# post specific the request
@support.route('/request/user/new', methods=['POST'])
@login_required
def post_request(current_user):

    if not current_user.admin:

        name = request.form['request_name']
        info = request.form['request_info']

        alphabet = string.ascii_letters + string.digits
        request_id = ''.join(random.choice(alphabet) for i in range(7))

        user = Users.query.filter_by(public_id=current_user.public_id).first()
        req = Requestuser(request_id=request_id,
                          req_name=name,
                          req=info,
                          status=False,
                          author=user)

        db.session.add(req)
        db.session.commit()

        return jsonify({'msg': 'Request Sent Successfully!!'})

    return make_response('Only Resident users can apply for support', 401)


# post specific the repair
@support.route('/repair/user/new', methods=['POST'])
@login_required
def post_repair(current_user):

    if not current_user.admin:
        name = request.form['repair_name']
        info = request.form['repair_info']

        alphabet = string.ascii_letters + string.digits
        repair_id = ''.join(random.choice(alphabet) for i in range(7))

        user = Users.query.filter_by(public_id=current_user.public_id).first()
        rep = Repairuser(repair_id=repair_id,
                         rep_name=name,
                         rep=info,
                         status=False,
                         author=user)

        db.session.add(rep)
        db.session.commit()

        return jsonify({'msg': 'Repair Sent Successfully!!'})

    return make_response('Only Resident users can apply for support', 401)


# update pending specific request
@support.route('/request/user/update', methods=['PUT'])
@login_required
def update_request(current_user):
    # the request status or the content can be updated by the resident user
    if not current_user.admin:
        # argument is given to update the status
        if request.args:
            data = request.args
            req = Requestuser.query.filter_by(request_id=data['req_id'])\
                .first()

            if data['status'] == '1':
                req.status = True
            elif data['status'] == '0':
                req.status = False

            db.session.commit()
            return({'request': req.req_name, 'status': req.status})
        # json is given to update the content
        if request.is_json:
            data = request.get_json()
            req = Requestuser.query.filter_by(request_id=data['req_id'])\
                .first()

            req.req_name = data['request_name']
            req.req = data['request_info']

            db.session.commit()

            return({'msg': 'updated successfully!!'})

        return({'msg': 'No argumnets given'})

    return make_response('Can only be edited by residents', 401)


# update pending specific repair
@support.route('/repair/user/update', methods=['PUT'])
@login_required
def update_repair(current_user):
    # the repair status or the content can be updated by the resident user
    if not current_user.admin:
        # argument is given to update the status
        if request.args:
            data = request.args
            rep = Repairuser.query.filter_by(repair_id=data['rep_id'])\
                .first()

            if data['status'] == '1':
                rep.status = True
            elif data['status'] == '0':
                rep.status = False

            db.session.commit()
            return({'repair': rep.rep_name, 'status': rep.status})
        # json is given to update the content
        if request.is_json:
            data = request.get_json()
            rep = Repairuser.query.filter_by(repair_id=data['rep_id'])\
                .first()

            rep.rep_name = data['repair_name']
            rep.rep = data['repair_info']

            db.session.commit()

            return({'msg': 'updated successfully!!'})

        return({'msg': 'No argumnets given'})

    return make_response('Can only be edited by residents', 401)


# delete completed request
@support.route('/request/remove', methods=['DELETE'])
@login_required
def delete_request(current_user):

    if request.args:
        data = request.args.get('req_id')
        req = Requestuser.query.filter_by(request_id=data).first()

        db.session.delete(req)
        db.session.commit()

        return({'msg': 'Deleted Successfully!!'})

    return make_response('No arguments Given!!')


# delete completed repair
@support.route('/repair/remove', methods=['DELETE'])
@login_required
def delete_repair(current_user):

    if request.args:
        data = request.args.get('rep_id')
        rep = Repairuser.query.filter_by(repair_id=data).first()

        db.session.delete(rep)
        db.session.commit()

        return({'msg': 'Deleted Successfully!!'})

    return make_response('No arguments Given!!')
