#!/usr/bin/env python3
"""
implements the sessionAuth class that
handles session authentication
"""
from api.v1.auth.auth import Auth
import uuid


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
