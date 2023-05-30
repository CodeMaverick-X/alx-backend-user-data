#!/usr/bin/env python3
"""
module that contains the authentication class
"""
from flask import request
from typing import List, TypeVar

class Auth:
    """authentication class to manage
    the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """authorized path"""
        return False

    def authorization_header(self, request=None) -> str:
        """authorize headers"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None
