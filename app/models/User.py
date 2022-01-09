from . import db, ma, bcrypt
import datetime



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def save(self):
        self.password = self.__generate_hash(self.password)
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        valid_fields = ('name', 'email', 'password')
        for key, value in data.items():
            if key == 'password':
                setattr(self, key, self.__generate_hash(value))

            if key in valid_fields:
                setattr(self, key, value)
        
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    # TODO: Add method to generate password hash
    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode('utf-8')

    # TODO: Add method to check password hash
    def check_hash(self, unhashed_password):
        return bcrypt.check_password_hash(self.password, unhashed_password)

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_one_user(id):
        return User.query.get(id)

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()
        # Also try
        # return User.query.get(email=email)

    def __repr__(self):
        return f'<User id: {self.id}>'


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'created_at', 'modified_at', 'blogposts')
        model = User

    blogposts = ma.Nested('BlogpostSchema', many=True, exclude=('user',))


class PublicUserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'blogposts')

    blogposts = ma.Nested('BlogpostSchema', many=True, exclude=('user',))


user_schema = UserSchema()
users_schema = UserSchema(many=True)

public_user_schema = PublicUserSchema()
public_users_schema = PublicUserSchema(many=True)
