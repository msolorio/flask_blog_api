from . import db, ma
import datetime

class Blogpost(db.Model):
    __tablename__ = 'blogposts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    contents = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Q: What is lazy
    user = db.relationship('User', backref=db.backref('blogposts', lazy=True))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        valid_fields = ('title', 'contents')
        for key, value in data.items():
            if key in valid_fields:
                setattr(self, key, value)
        
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    @staticmethod
    def get_all_blogposts():
        return Blogpost.query.all()

    @staticmethod
    def get_one_blogpost(id):
        return Blogpost.query.get(id)

    def __repr__(self):
        return f'<Blogpost id: {self.id}>'


class BlogpostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'contents', 'created_at', 'modified_at', 'user_id')
        model = Blogpost
        include_fk = True


blogpost_schema = BlogpostSchema()
blogposts_schema = BlogpostSchema(many=True)
