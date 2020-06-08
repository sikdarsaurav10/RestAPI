from flask import Blueprint, jsonify, request, make_response
from webApp import db
from webApp.models import Users, Post, Comments, Likemeter
from webApp.utils import login_required, save_post

post = Blueprint('Posts', __name__)


# get all the posts
@post.route('/', methods=['GET'])
@login_required
def get_all_post(current_user):

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=10)

    output = []

    for post in posts.items:
        output_data = {}
        output_com = []
        com_data = {}
        output_like = []
        like_data = {}
        output_data['post_img'] = post.post_img
        output_data['caption'] = post.caption
        output_data['date_posted'] = post.date_posted
        com = Comments.query.filter_by(posted=post).all()
        for i in com:
            com_data[i.Commentor] = i.comm
            output_com.append(com_data)
        output_data['Comments'] = output_com
        like = Likemeter.query.filter_by(posted=post).all()
        for y in like:
            user = Users.query.filter_by(public_id=y.liker).first()
            like_data[user.name] = y.like_meter
        output_like.append(like_data)
        output_data['Likes'] = output_like
        user = Users.query.filter_by(public_id=post.user_id).first()
        output_data['Post uploaded by'] = user.name
        output.append(output_data)

    return jsonify({'posts': output})


# get the post uploaded by the specific users
@post.route('/user', methods=['GET'])
@login_required
def get_user_post(current_user):

    page = request.args.get('page', 1, type=int)

    user = Users.query.filter_by(public_id=current_user.public_id).first()
    posts = Post.query.order_by(Post.date_posted.desc()).filter_by(author=user)\
        .paginate(page=page, per_page=10)

    output = []

    for post in posts.items:
        output_data = {}
        output_com = []
        com_data = {}
        output_like = []
        like_data = {}
        output_data['post_img'] = post.post_img
        output_data['caption'] = post.caption
        output_data['date_posted'] = post.date_posted
        com = Comments.query.filter_by(posted=post).all()
        for i in com:
            com_data[i.Commentor] = i.comm
            output_com.append(com_data)
        output_data['Comments'] = output_com
        like = Likemeter.query.filter_by(posted=post).all()
        for y in like:
            user = Users.query.filter_by(public_id=y.liker).first()
            like_data[user.name] = y.like_meter
        output_like.append(like_data)
        output_data['Likes'] = output_like
        output.append(output_data)

    return jsonify({'posts': output})


# upload post uploaded by the specific users
@post.route('/user/new', methods=['POST'])
@login_required
def upload_user_post(current_user):

    file_name = request.files['file']
    postCap = request.form['caption']
    file_t = save_post(file_name)
    user = Users.query.filter_by(public_id=current_user.public_id).first()
    post = Post(post_img=file_t, caption=postCap, author=user)

    db.session.add(post)
    db.session.commit()

    return jsonify({'message': 'Post uploaded', 'img': file_t})


# get the post deleted by the specific users
@post.route('/user/remove', methods=['DELETE'])
@login_required
def delete_user_post(current_user):

    if request.args:
        data = request.args

        user = Users.query.filter_by(public_id=current_user.public_id).first()
        post = Post.query.filter_by(author=user)\
            .filter_by(post_img=data['post'])\
            .first()

        db.session.delete(post)
        db.session.commit()

        return jsonify({'message': 'Post Deleted'})

    return make_response('User not valid', 401)


# increase the count
@post.route('/', methods=['POST'])
@login_required
def update_likes(current_user):

    if request.args:
        data = request.args.get('post')

        user = Users.query.filter_by(public_id=current_user.public_id)\
            .first()
        post = Post.query.filter_by(post_img=data).first()
        likes = Likemeter.query.filter_by(posted=post).all()

        if len(likes) != 0:
            for like in likes:
                if user.public_id not in like.liker:
                    liked = Likemeter(like_meter=True,
                                      liker=user.public_id,
                                      like_id=post.id)
                    db.session.add(liked)

        elif len(likes) == 0:
            liked = Likemeter(like_meter=True,
                              liker=user.public_id,
                              like_id=post.id)
            db.session.add(liked)

        db.session.commit()

        return jsonify({'msg': 'post liked'})


# add comments to the post
@post.route('/comm', methods=['POST'])
@login_required
def update_comm(current_user):

    if request.is_json:
        data = request.get_json()
        post = request.args.get('post')

        user = Users.query.filter_by(public_id=current_user.public_id)\
            .first()
        post = Post.query.filter_by(post_img=post).first()
        comm = Comments(comm=data['comments'],
                        Commentor=user.name,
                        post_id=post.id)

        db.session.add(comm)
        db.session.commit()

        return jsonify({'msg': 'commented successfully!!'})
