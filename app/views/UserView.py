from flask import Blueprint, request, jsonify
from ..models import user_schema, users_schema, User
from ..utils.has_all_required_fields import has_all_required_fields

user_bp = Blueprint('users', __name__)

@user_bp.route('/')
def index_users():
    all_users = User.query.all()

    return jsonify(users_schema.dump(all_users))


@user_bp.route('/<int:user_id>')
def show_users(user_id):
    user = User.query.get(user_id)

    if not user:
        return { 'message': 'No user with that id found' }

    print('user ==>', user)
    print('user.blogposts ==>', user.blogposts)

    return user_schema.dump(user)


@user_bp.route('/', methods=['POST'])
def create_users():
    req_data = request.get_json()
    
    valid, field = has_all_required_fields(req_data, ('name', 'email', 'password'))

    if not valid:
        return { 'message': f'{field} is a required field' }, 400

    user_in_db = User.get_user_by_email(req_data.get('email'))
    if user_in_db:
        return { 'message': 'user with that email already exists' }, 400

    user = User(
        name=req_data.get('name'),
        email=req_data.get('email'),
        password=req_data.get('password')
    )
    user.save()

    # TODO: generate authentication token to return to client

    return user_schema.dump(user)


# TODO: Get all blogposts for a particular user