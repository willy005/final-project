from piches import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    pitches = db.relationship('Pitch', backref='author', lazy=True)

    def __repr__(self):
        # return f"User('{self.username}, {self.email}, {self.image_file}')"
        return "User {}, {}".format(self.username, self.image_file)


class Pitch(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(200), nullable=False)
    pitch = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='commenter', lazy=True)

    def __repr__(self):
        # return f"Pitch('{self.pitch}, {self.date_posted}')"
        return "Pitch {}, {}".format(self.pitch, self.date_posted)


class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitch.id'), nullable=False)

    def __repr__(self):
        # return f"Pitch('{self.comment}, {self.date_posted}')"
        return "Pitch {}, {}".format(self.comment, self.date_posted)