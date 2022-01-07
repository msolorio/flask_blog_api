export FLASK_APP=run:app
export FLASK_ENV=development
export JWT_SECRET_KEY=thisisasecret
export SQLALCHEMY_DATABASE_URI=postgresql://michael@localhost:5432/flask_blog_db

pipenv shell

flask run -h 0.0.0.0
