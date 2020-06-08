import random
import string
from flask import Blueprint, jsonify, request, url_for, make_response
from webApp import db
from webApp.models import CabService
from webApp.utils import save_cab_pic, login_required

cab = Blueprint('Cab', __name__)


# to save a new cab record
@cab.route('/cab_details/new', methods=['POST'])
@login_required
def create_cab(current_user):

    if not current_user.admin:
        return make_response('Not permitted!!', 401)

    data = request.get_json()
    alphabet = string.ascii_letters + string.digits
    cab_id = ''.join(random.choice(alphabet) for i in range(8))

    newCab = CabService(cab_id=cab_id,
                        name=data['name'],
                        descp=data['description'],
                        contact=data['contact'])

    db.session.add(newCab)
    db.session.commit()

    return jsonify({'message': 'Cab Record saved'})


# upload the image for the cab services
@cab.route('/cab_prof_pic/upload/<cab_id>', methods=['PUT'])
@login_required
def upload_cab_img(current_user, cab_id):

    if not current_user.admin:
        return make_response('Not permitted!!', 401)

    file_name = request.files['file']
    file_t = save_cab_pic(file_name)
    user = CabService.query.filter_by(cab_id=cab_id).first()
    user.prof_img = file_t

    db.session.commit()

    return jsonify({'message': 'File saved successfully',
                    'file name': file_t})


# to get the cab profile pic
@cab.route('/cab_prof_pic/<cab_id>', methods=['GET'])
def get_cab_prof_pic(cab_id):
    img_query = CabService.query.filter_by(cab_id=cab_id).first()
    image_file = url_for('static', filename='images/cab_service_img/' + img_query.prof_img)
    return jsonify({'cab_prof_img_url': image_file})


# to get all the cab services
@cab.route('/cab_details', methods=['GET'])
@login_required
def get_cabs(current_user):

    page = request.args.get('page', 1, type=int)
    allCabs = CabService.query.paginate(page=page, per_page=10)

    output = []

    for cabs in allCabs.items:
        output_data = {}
        output_data['Cab_id'] = cabs.cab_id
        output_data['name'] = cabs.name
        output_data['desription'] = cabs.descp
        output_data['contact'] = cabs.contact
        output_data['prof_img'] = cabs.prof_img
        output.append(output_data)

    return jsonify({'All Cabs': output})


# to update a cab record
@cab.route('/cab_details/update/<cab_id>', methods=['PUT'])
@login_required
def update_cab(current_user, cab_id):

    if not current_user.admin:
        return make_response('Not permitted!!', 401)

    cab = CabService.query.filter_by(cab_id=cab_id).first_or_404()

    data = request.get_json()

    cab.name = data['name']
    cab.descp = data['description']
    cab.contact = data['contact']

    db.session.commit()

    return jsonify({'message': 'Cab Record saved'})


# to delete a cab record
@cab.route('/cab_details/remove', methods=['DELETE'])
@login_required
def delete_cab(current_user):

    if not current_user.admin:
        return make_response('Not permitted!!', 401)

    if request.args:
        data = request.args.get('cab_id')

        cab = CabService.query.filter_by(cab_id=data).first_or_404()

        db.session.delete(cab)
        db.session.commit()

        return jsonify({'message': 'Cab Record deleted'})

    return make_response('No argument given!', 401)
