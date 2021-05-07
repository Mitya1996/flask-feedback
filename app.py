"""Flask Feedback application."""

from flask import Flask, render_template, redirect, request, flash, session, url_for
from models import db, connect_db, User, Feedback
from forms import AddUserForm, LoginForm, FeedbackForm

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

        session['username'] = new_user.username

        flash(f"{new_user.username} registered successfully")
        return redirect(url_for('secret', username=new_user.username))

    return render_template('register.html', form=form)

@app.route('/users/<username>')
def secret(username):
    user = User.query.get_or_404(username)
    curr_user = session.get('username')    
    if "username" not in session:
        flash("you must be logged in to view this page")
        return redirect("/")
    if curr_user != user.username:
        flash("you are unauthorized to view this page")
        return redirect(f'/users/{curr_user}')

    return render_template('secret.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if not user:
            flash("invalid credentials")
            return redirect('/login')
        #else if all good    
        session['username'] = user.username
        flash(f"{username} logged in successfully")
        return redirect(url_for('secret', username=user.username))

    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("username")

    return redirect("/")

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Deletes user."""
    #authorization
    curr_user = session.get('username')
    if curr_user != username:
        flash("you are unauthorized to delete users other than yourself")
        return redirect(f'/')

    User.query.filter_by(username=username).delete()
    db.session.commit()
    flash(f"user deleted successfully")
    return redirect('/logout')


@app.route("/users/<username>/feedback/add", methods=['GET', 'POST'])
def add_feedback(username):
    """Add new feedback for given user."""
    #authorization
    curr_user = session.get('username')
    if curr_user != username:
        flash("you are unauthorized create posts for other users")
        return redirect('/')

    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        flash(f"feedback added successfully")
        return redirect(f'/users/{username}')
    return render_template('new-feedback.html', username=username, form=form)


@app.route('/feedback/<id>/delete')
def delete_feedback(id):
    username = session.get('username')
    user = User.query.get(username)
    feedback = Feedback.query.get_or_404(id)
    if username != feedback.user.username:
        flash("you are unauthorized to delete other users' feedback")
        return redirect(f'/')

    Feedback.query.filter_by(id=id).delete()
    db.session.commit()
    flash(f"feedback deleted")
    if username:
        return redirect(f'/users/{username}')
    else:
        return redirect('/')


@app.route('/feedback/<id>/update', methods=['GET', 'POST'])
def update_feedback(id):
    feedback = Feedback.query.get_or_404(id)
    username = feedback.user.username

    #authorization
    curr_user = session.get('username')
    if curr_user != username:
        flash("you are unauthorized update feedback for other users")
        return redirect('/')

    form = FeedbackForm()
    if request.method == 'GET':
        form.title.data = feedback.title
        form.content.data = feedback.content

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        flash(f"feedback updated")
        return redirect(f'/users/{username}')

    return render_template('update-feedback.html', form=form, feedback=feedback)