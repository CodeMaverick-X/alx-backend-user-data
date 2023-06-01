#!/usr/bin/env python3
"""
module that contains the authentication class
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """authentication class to manage
    the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Ensures that a route user is authenticated
        """
        if path is None:
            return True
        if excluded_paths is None:
            return True
        if path.endswith('/'):
            path = path[0: -1]
        if path in excluded_paths or path + '/' in excluded_paths\
                or self.wild_path_match(path, excluded_paths):
            return False
        return True

    def wild_path_match(self, path: str, excluded_paths: List[str]) -> bool:
        """match wild character"""
        for d in excluded_paths:
            if d.endswith("*"):
                if path[:len(d) - 1] + '*' == d:
                    return True
        return False

    def authorization_header(self, request=None) -> str:
        """authorize headers"""
        if not request or 'Authorization' not in request.headers.keys():
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None

    def session_cookie(self, request=None):
        """return cookie from request obj"""

        if not request:
            return None
        _my_session_id = getenv('SESSION_NAME')
        return request.cookies.get(_my_session_id)
