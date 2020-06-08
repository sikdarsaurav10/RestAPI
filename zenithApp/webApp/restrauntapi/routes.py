import random
import string
from flask import Blueprint, jsonify, request, url_for, make_response
from webApp import db
from webApp.models import Food, Menu
from webApp.utils import save_rest_pic, login_required

food = Blueprint('Food', __name__)


# to save or push a new restraunt record
@food.route('/food_details/new', methods=['POST'])
@login_required
def create_food(current_user):

    if not current_user.admin:
        return make_response('Not permitted!!', 401)

    data = request.get_json()
    alphabet = string.ascii_letters + string.digits
    restraunt_id = ''.join(random.choice(alphabet) for i in range(10))

    newFood = Food(restraunt_id=restraunt_id,
                   name=data['name'],
                   descp=data['description'],
                   contact=data['contact'])

    db.session.add(newFood)
    db.session.commit()

    return jsonify({'message': 'Restraunt Record saved'})


# to update a restraunt record in the database
@food.route('/food_details/<restraunt_id>', methods=['PUT'])
@login_required
def update_food(current_user, restraunt_id):

    if not current_user.admin:
        return make_response('Not permitted!!', 401)

    rest = Food.query.filter_by(restraunt_id=restraunt_id)\
        .first()

    if not rest:
        return jsonify({'message': 'NO RESTRAUNT FOUND!!'})

    data = request.get_json()

    rest.name = data['name']
    rest.descp = data['description']
    rest.contact = data['contact']

    db.session.commit()

    return jsonify({'message': 'Restraunt Record updated'})


# to delete a restraunt record in the database
@food.route('/food_details/remove', methods=['DELETE'])
@login_required
def delete_food(current_user):

    if not current_user.admin:
        return make_response('Not permitted!!', 401)

    if request.args:
        data = request.args.get('restraunt_id')
        rest = Food.query.filter_by(restraunt_id=data).first_or_404()

        db.session.delete(rest)
        db.session.commit()

        return jsonify({'message': 'Restraunt Record deleted'})

    return ('No argumnets given', 401)


# upload the image for the Restraunt services
@food.route('/food_prof_pic/upload/<restraunt_id>', methods=['PUT'])
@login_required
def upload_food_img(current_user, restraunt_id):

    if not current_user.admin:
        return make_response('Not permitted!!', 401)

    file_name = request.files['file']
    file_t = save_rest_pic(file_name)
    user = Food.query.filter_by(restraunt_id=restraunt_id).first_or_404()
    user.prof_img = file_t

    db.session.commit()

    return jsonify({'message': 'File saved successfully',
                    'file name': file_t})


# to get the restraunt profile pic
@food.route('/food_prof_pic/<restraunt_id>', methods=['GET'])
def get_rest_prof_pic(restraunt_id):
    img_query = Food.query.filter_by(restraunt_id=restraunt_id).first()
    image_file = url_for('static', filename='images/restraunt_service_img/' + img_query.prof_img)
    return jsonify({'restraunt_prof_img_url': image_file})


# to get all the Restraunt services
@food.route('/food_details', methods=['GET'])
@login_required
def get_rest(current_user):

    page = request.args.get('page', 1, type=int)
    allFood = Food.query.paginate(page=page, per_page=10)

    output = []

    for rest in allFood.items:
        output_data = {}
        output_data['restraunt_id'] = rest.restraunt_id
        output_data['name'] = rest.name
        output_data['desription'] = rest.descp
        output_data['contact'] = rest.contact
        output_data['prof_img'] = rest.prof_img
        output.append(output_data)

    return jsonify({'All Restraunts': output})


# get the menu for the specific restraunt
@food.route('/food_menu/<restraunt_id>', methods=['GET'])
@login_required
def get_food_menu(current_user, restraunt_id):

    rest = Food.query.filter_by(restraunt_id=restraunt_id).first()
    menuItem = Menu.query.filter_by(restraunt=rest).all()

    output = []

    for item in menuItem:
        output_data = {}
        output_data['id'] = item.id
        output_data['food_item'] = item.food_item
        if not item.item_type:
            output_data['Type'] = 'Veg'
        elif item.item_type:
            output_data['Type'] = 'Non Veg'
        output.append(output_data)

    return jsonify({'Menu': output})


# upload the menu for the specific restraunt
@food.route('/food_menu/new/<restraunt_id>', methods=['POST'])
@login_required
def upload_food_menu(current_user, restraunt_id):

    if not current_user.admin:
        return make_response('Not permitted!!', 401)

    if request.is_json:
        data = request.get_json()
        rest = Food.query.filter_by(restraunt_id=restraunt_id).first()

        menu = Menu(food_item=data['item'], item_type=data['type'],
                    restraunt=rest)
        db.session.add(menu)
        db.session.commit()

        return jsonify({'message': 'Saved', 'Item': data['item']})

    return make_response('No Menu Items given', 401)


# delete the menu for the specific restraunt
@food.route('/food_menu/remove/<restraunt_id>', methods=['DELETE'])
@login_required
def delete_food_menu(current_user, restraunt_id):

    if not current_user.admin:
        return make_response('Not permitted!!', 401)

    if request.args:
        data = request.args
        rest = Food.query.filter_by(restraunt_id=restraunt_id)\
            .first_or_404()
        id = data['id']
        menu = Menu.query.filter_by(restraunt=rest).filter(Menu.id == id)\
            .first()

        db.session.delete(menu)
        db.session.commit()

        return jsonify({'message': 'deleted'})

    return make_response('No Menu Items given', 401)
