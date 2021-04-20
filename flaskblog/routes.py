import secrets, os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt
# Once the email and password is valdiated and the user exists in the database,
# This package is used to login into website.
from flask_login import login_user, current_user, logout_user, login_required

# It is like a home page to our web-site
@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)#default value is 1.
    # order_by(Post.date_posted.desc())-> to view latest post first
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("home.html", posts=posts)

@app.route('/about')
def about():
    return render_template("about.html", title='about')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # checks if the
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Decrypt the password entered by user using bcrypt
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # Add the information entered by user in database
        db.session.add(user)
        # Commit changes entered by the user in database
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in!', 'success')
        return redirect(url_for('login'))#name of home function
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))# check if keyword next is there in URL.
        else:
            flash(f'Login Unsuccessful! Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# logout for a User
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # REsize the image to 125*125 px
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

# User Account page
@app.route('/account', methods=['GET', 'POST'])
# Since we can directly navigate pages using url's,
# so this will avoid those scenarios since to view the account page, the user needs to login first.
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        # Update the db values using form values.
        current_user.username= form.username.data
        current_user.email= form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename= 'profile_pics/'+ current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form)

# Posts
@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # Adding the data entered in new post form into the database.
        post = Post(title=form.title.data, content= form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend= "New Post")


@app.route('/post/<int:post_id>')
def post(post_id):
    # get the data if it exists or else throw 404 error.
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author!=current_user:
        # Forbidden route
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method=='GET':
        # We want the already feeded data to be there in title and content while updating the post.
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend="Update Post")

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author!=current_user:
        # Forbidden route
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)#default value is 1.
    user=User.query.filter_by(username=username).first_or_404()
    # order_by(Post.date_posted.desc())-> to view latest post first
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=4)
    return render_template("user_posts.html", posts=posts, user=user)
