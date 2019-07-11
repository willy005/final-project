from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from piches.models import User


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(),
                                                   Length(min=2, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired()
                                         , EqualTo('password')])

    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username already taken')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email already registered')


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class PitchForm(FlaskForm):
    category = StringField('category', validators=[DataRequired()])
    pitch = TextAreaField('pitch', validators=[DataRequired()])
    submit = SubmitField('Pitch')


class CommentForm(FlaskForm):
    comment = TextAreaField('comment', validators=[DataRequired()])
    submit = SubmitField('Comment')


class UpdateAccountForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(),
                                                   Length(min=2, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('The username is already taken choose another one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('The email is already taken try another one')
