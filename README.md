## Flask API Demo

To be used as a reference for new Flask projects

- Authentication and authorization w/JWT
- One to many related model creation

- Flask
- SQLAlchemy
- Marshmallow
- PostgreSQL
- Flask Migrate

---

## Steps to Run

Create a postgres database
$ createdb flask_postgres

Create Tables in PostgreSQL
$ ./migrate 'Initial migration'

Run the Bootsrap
$ ./bootstrap.sh

This will

    set necessary environment variables
    start virtual environment
    create app
    run app at http://localhost:5000

---

Signup a new user - returns a JWT
`POST /users/ { 'name': 'Carl', 'email': 'carl@sagan.net', 'password': 'vastness' }`

Login - returns a JWT
`POST /users/login/ { 'email': 'carl@sagan.net', 'password': 'vastness' }

Get all users and their blogposts - sending request header 'api-token' --> 'your token'
`GET /users/`

Get a single user and their blogposts - sending request header 'api-token' --> 'your token'
`GET /users/<int:user_id>`
