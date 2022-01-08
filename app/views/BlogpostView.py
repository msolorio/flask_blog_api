from flask import Blueprint, request, jsonify
from ..models import blogpost_schema, blogposts_schema, Blogpost
from ..utils.has_all_required_fields import has_all_required_fields

blogpost_bp = Blueprint('blogposts', __name__)

@blogpost_bp.route('/')
def index_blogpost():
    all_blogposts = Blogpost.query.all()

    return jsonify(blogposts_schema.dump(all_blogposts))


@blogpost_bp.route('/<int:blogpost_id>')
def show_blogpost(blogpost_id):
    blogpost = Blogpost.query.get(blogpost_id)

    if not blogpost:
        return { 'message': 'No blogpost with that id found' }

    return blogpost_schema.dump(blogpost)


@blogpost_bp.route('/', methods=['POST'])
def create_blogpost():
    req_data = request.get_json()

    valid, field = has_all_required_fields(req_data, ('title', 'contents', 'user_id'))

    if not valid:
        return { 'message': f'{field} is a required field' }, 400

    blogpost = Blogpost(
        title=req_data.get('title'),
        contents=req_data.get('contents'),
        user_id=req_data.get('user_id')
    )

    blogpost.save()

    return blogpost_schema.dump(blogpost)
