"""Models for Flask Feedback."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        primary_key=True,
        unique=True
        )
    password = db.Column(
        db.Text,
        nullable=False
        )
    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True
        )
    first_name = db.Column(
        db.String(30),
        nullable=False
        )
    last_name = db.Column(
        db.String(30),
        nullable=False
        )

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False


    class Feedback(db.Model):
        """Feedback."""

        __tablename__ = "feedback"

        # id - a unique primary key that is an auto incrementing integer
        id = db.Column(
            db.Integer,
            auto_incrementing=True,
            unique=True,
            primary_key=True
        )
        # title - a not-nullable column that is at most 100 characters
        title = db.Column(
            db.String(100),
            nullable=False
        )
        # content - a not-nullable column that is text
        content = db.Column(
            db.Text,
            nullable=False
        )
        # username - a foreign key that references the username column in the users table
        username = db.Column(
            db.String(20),
            db.ForeignKey('users.username', ondelete='CASCADE')
            )