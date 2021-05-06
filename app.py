"""Flask Feedback application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User
from forms import AddUserForm, LoginForm
import bcrypt

app = Flask(__name__)

# DebugToolbarExtension code str8 from docs
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:myPassword@localhost:5432/feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')
def home():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = AddUserForm()
    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_user = User.register(**data)

        db.session.add(new_user)
        db.session.commit()

        flash(f"{new_user.username} registered successfully.")
        return redirect('/secret')

    return render_template('register.html', form=form)

@app.route('/secret')
def secret():
    return render_template('secret.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if not user:
            flash("Invalid credentials.")
            return redirect('/login')
        flash(f"{username} logged in successfully.")
        return redirect('/secret')

    return render_template('login.html', form=form)