from flask import render_template, url_for, flash, redirect, request
from piches.forms import RegistrationForm, LoginForm, PitchForm, CommentForm, UpdateAccountForm
from piches.models import User, Pitch, Comment
from piches import app, db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
@app.route('/home')
def home():
    pitches = Pitch.query.all()
    return render_template('home.html', pitches=pitches, title="Home")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        send_email(form.email.data)
        flash('Your account has been created, please check your email!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title="Register", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Wrong login credentials", 'danger')

    return render_template('login.html', title="Login", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def send_email(email):
    pass


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account has been updated')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile/' + current_user.image_file)
    pitches = Pitch.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', title="profile", pitches=pitches, image_file=image_file, form=form)


@app.route('/categories')
@login_required
def categories():
    pitches = Pitch.query.distinct().all()
    return render_template('categories.html', title="categories", pitches=pitches)


@app.route('/pitch/new', methods=['GET', 'POST'])
@login_required
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        pitch = Pitch(category=form.category.data, pitch=form.pitch.data,
                      author=current_user)

        db.session.add(pitch)
        db.session.commit()
        flash('Your pitch has been created', 'success')
        return redirect(url_for('home'))
    return render_template('new_pitch.html', title="New Pitch", form=form)


@app.route('/comment/<int:pitch_id>', methods=['GET', 'POST'])
def new_comment(pitch_id):
    comments = Comment.query.filter_by(pitch_id=pitch_id)
    form = CommentForm()
    if form.validate_on_submit():

        comment = Comment(comment=form.comment.data, pitch_id=pitch_id)

        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added', 'success')
        return redirect(url_for('home'))
    return render_template('new_comment.html', title="New Comment", form=form, comments=comments)
