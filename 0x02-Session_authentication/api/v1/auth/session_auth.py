#!/usr/bin/env python3
"""
implements the sessionAuth class that
handles session authentication
"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """session auth class"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session id"""
        if not user_id or type(user_id) != str:
            return None

        sess_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[sess_id] = user_id
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a user_id based on sess_id"""

        if not session_id or type(session_id) != str:
            return None

        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns the user based"""
        sess_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(sess_id)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """destroy session"""

        if not request:
            return None
        sess_id = self.session_cookie(request)
        if not sess_id:
            return False
        user_id = self.user_id_for_session_id(sess_id)
        if not user_id:
            return False
        del self.user_id_by_session_id[sess_id]
        return True
