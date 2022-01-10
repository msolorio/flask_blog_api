from flask import Blueprint, request, jsonify
import datetime
from ..models import public_user_schema, public_users_schema, User, user_schema
from ..shared.Authentication import Auth
from ..utils.has_all_required_fields import has_all_required_fields

user_bp = Blueprint('users', __name__)

@user_bp.route('/')
@Auth.auth_required
def index_users():
    all_users = User.query.all()

    return jsonify(public_users_schema.dump(all_users))


@user_bp.route('/<int:user_id>')
@Auth.auth_required
def show_users(user_id):
    user = User.query.get(user_id)

    if not user:
        return { 'message': 'No user with that id found' }

    return public_user_schema.dump(user)



@user_bp.route('/', methods=['POST'])
def signup():
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
        password=req_data.get('password'),
        created_at=datetime.datetime.utcnow(),
        modified_at=datetime.datetime.utcnow()
    )
    user.save()

    serialized_data = user_schema.dump(user)
    token = Auth.generate_token(serialized_data.get('id'))

    return { 
        'user': public_user_schema.dump(user),
        'jwt_token': token
    }, 200



@user_bp.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()

    if not req_data.get('email') or not req_data.get('password'):
        return { 'error': 'email and password are required' }, 400

    user = User.get_user_by_email(req_data.get('email'))

    if not user or not user.check_hash(req_data.get('password')):
        return { 'error': 'invalid credentails' }, 400

    serialized_data = user_schema.dump(user)
    token = Auth.generate_token(serialized_data.get('id'))

    return { 'jwt_token': token }, 200

# TODO: Get all blogposts for a particular user