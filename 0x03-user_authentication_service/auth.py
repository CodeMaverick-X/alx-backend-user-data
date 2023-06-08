#!/usr/bin/env python3
"""contains a fincion that hashes pass with bcrypt"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """hash user password"""
    bytes_s = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_p = bcrypt.hashpw(bytes_s, salt)
    return hash_p


def _generate_uuid() -> str:
    """generate and return uuid"""
    return str(uuid.uuid4())


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
            hashed_p = _hash_password(password)
            return self._db.add_user(email, hashed_p)
        else:
            raise ValueError('User {} already exists'.format(user.email))

    def valid_login(self, email: str, password: str) -> bool:
        """validate a user"""
        bytes_p = password.encode('utf-8')
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound):
            return False
        else:
            return bcrypt.checkpw(bytes_p, user.hashed_password)

    def create_session(self, email: str) -> str:
        """create and store session id for user"""
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound):
            return
        else:
            sess_id = _generate_uuid()
            self._db.update_user(user.id, session_id=sess_id)
            return sess_id

    def get_user_from_session_id(session_id: str) -> Union[User, None]:
        """get a user for a given session id"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except (NoResultFound):
            return None
        else:
            return user
