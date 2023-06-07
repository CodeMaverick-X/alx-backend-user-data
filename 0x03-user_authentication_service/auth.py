#!/usr/bin/env python3
"""contains a fincion that hashes pass with bcrypt"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hash user password"""
    bytes_s = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_p = bcrypt.hashpw(bytes_s, salt)
    return hash_p


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a new user"""
        user = ''
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound):
            pass
        else:
            raise ValueError('User {} already exists'.format(user.email))

        hashed_p = _hash_password(password)
        self._db.add_user(email, hashed_p)
        return user
