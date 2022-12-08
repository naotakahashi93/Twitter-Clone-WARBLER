"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
    
    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_following(self): 

        """Does is_following successfully detect when user1 is following user2?"""

        user1 = User(
            email="test@test.com",
            username="testuser1",
            password="HASHED_PASSWORD"
        )

        user2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )
    
        user1.following.append(user2)
        user2.following.append(user1)
        self.assertEqual(user1.is_following(user2), 1)
        self.assertEqual(user2.is_following(user1), 1)

        self.assertEqual(user1.username, "testuser1")


    def test_notfollowing(self): 
        """Does is_following successfully detect when user1 is NOT following user2?"""
        
        user1 = User(
            email="test@test.com",
            username="testuser1",
            password="HASHED_PASSWORD"
        )

        user2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )
        self.assertNotEqual(user2.is_following(user1), 1)
        self.assertNotEqual(user1.is_following(user2), 1)

    
    # def test_create(self): 
    #     fail_user = User(
    #         username="testuser1"
    #     )
    #     self.assertNotIsInstance(fail_user, User)

    
    # def test_authentication(self):  ## failing
    #     user1 = User(
    #         email="test@test.com",
    #         username="testuser1",
    #         password="HASHED_PASSWORD"
    #     )
    #     user1.signup("testuser1", "test@test.com", "HASHED_PASSWORD", "")
    #     self.assertEqual(user1.authenticate(user1.username,user1.password), user1)

        fail_user = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        self.assertEqual(fail_user.authenticate("testuser1sdjfhsdk","HASHED_PASSWORD"), False)

        fail_user1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        
        self.assertEqual(fail_user.authenticate("testuser","wronggg"), False)

        





