from . import db, ma
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
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        valid_fields = ('name', 'email', 'password')

        for key, value in data.items():
            if key in valid_fields:
                setattr(self, key, value)
        
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_one_user(id):
        return User.query.get(id)

    def __repr__(self):
        return f'<User id: {self.id}>'


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'created_at', 'modified_at')
        model = User


user_schema = UserSchema()
users_schema = UserSchema(many=True)
