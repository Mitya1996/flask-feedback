"""Seed file to make sample data for feedback db."""

from models import db, User, Feedback
from app import app

def seed_db():
    # Create all tables
    db.drop_all()
    db.create_all()

    # If table isn't empty, empty it
    User.query.delete()
    Feedback.query.delete()

    # Add users
    user1 = User.register('js', 'lol', 'j@j.com', 'John', 'Smith')
    user2 = User.register('css', 'lol', 'c@j.com', 'Cassie Sally', 'Smith')
    db.session.add_all([user1, user2])
    db.session.commit()

    # Add posts
    feedback1 = Feedback(title='My First Post', content='Hello world!', username='js')
    db.session.add(feedback1)
    db.session.commit()
 


seed_db()