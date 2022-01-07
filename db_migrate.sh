export FLASK_APP=run:app
export SQLALCHEMY_DATABASE_URI=postgresql://michael@localhost:5432/flask_blog_db

pipenv shell

flask db migrate -m '$1'
flask db upgrade
