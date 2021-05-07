from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory, Unique
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, NumberRange, Length
# The variable db here is a SQLAlchemy object instance from
# Flask-SQLAlchemy package
from models import db, User

BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

class AddUserForm(ModelForm):
    """Form for adding users."""

    username = StringField("Username",
        validators=[InputRequired(), Unique(User.username), Length(max=20)])
    password = PasswordField("Password",
        validators=[InputRequired()])
    email = StringField("Email",
        validators=[InputRequired(), Unique(User.email), Length(max=50)])
    first_name = StringField("First Name",
        validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name",
        validators=[InputRequired(), Length(max=30)])


class LoginForm(ModelForm):
    """Form for logging in."""

    username = StringField("Username",
        validators=[InputRequired()])
    password = PasswordField("Password",
        validators=[InputRequired()])

class FeedbackForm(ModelForm):
    """Form for feedback."""
    title = StringField("Title",
        validators=[InputRequired(), Length(max=100)])
    content = TextAreaField("Content",
        validators=[InputRequired()])




