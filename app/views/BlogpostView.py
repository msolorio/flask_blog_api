from flask import Blueprint, request, jsonify, g
import datetime
from ..models import blogpost_schema, blogposts_schema, Blogpost
from ..shared.Authentication import Auth
from ..utils.has_all_required_fields import has_all_required_fields

blogpost_bp = Blueprint('blogposts', __name__)

@blogpost_bp.route('/')
@Auth.auth_required
def index_blogpost():
    all_blogposts = Blogpost.query.all()

    return jsonify(blogposts_schema.dump(all_blogposts)), 200


@blogpost_bp.route('/<int:blogpost_id>')
@Auth.auth_required
def show_blogpost(blogpost_id):
    blogpost = Blogpost.query.get(blogpost_id)

    if not blogpost:
        return { 'message': 'No blogpost with that id found' }, 400

    return blogpost_schema.dump(blogpost), 200


@blogpost_bp.route('/', methods=['POST'])
@Auth.auth_required
def create_blogpost():
    req_data = request.get_json()

    valid, field = has_all_required_fields(req_data, ('title', 'contents'))

    if not valid:
        return { 'message': f'{field} is a required field' }, 400

    # Assigns user_id to logged in user
    blogpost = Blogpost(
        title=req_data.get('title'),
        contents=req_data.get('contents'),
        user_id=g.user.get('id'),
        created_at=datetime.datetime.utcnow(),
        modified_at=datetime.datetime.utcnow()
    )

    blogpost.save()

    return blogpost_schema.dump(blogpost), 201
