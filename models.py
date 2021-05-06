"""Models for Flask Feedback."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
        unique=True)
    password = db.Column(
        db.Text,
        nullable=False)
    email = db.Column(
        db.String(50),
        unique=True)
    first_name = db.Column(
        db.String(30),
        nullable=False)
    last_name = db.Column(
        db.String(30),
        nullable=False)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'