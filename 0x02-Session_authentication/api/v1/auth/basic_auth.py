#!/usr/bin/env python3
"""
implements the basic authentication
"""
import base64
from api.v1.auth.auth import Auth
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """class that implements the basic auth"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract the authorisation str from header"""
        if not authorization_header or\
           type(authorization_header) != str or\
           not authorization_header.startswith('Basic '):
            return None

        return authorization_header.split()[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """decode the auth str from header"""
        if not base64_authorization_header or\
           type(base64_authorization_header) != str:
            return None
        try:
            return base64.b64decode(base64_authorization_header)\
                   .decode('utf-8')
        except (Exception):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str) \
            -> Tuple[str, str]:
        """returns the user email and password from the Base64
        decoded value"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        data = decoded_base64_authorization_header.split(":")
        return data[0], ":".join(data[1:])

    def user_object_from_credentials(self, user_email:
                                     str, user_pwd: str) -> TypeVar('User'):
        """return instance of user for that email and pass"""
        if not user_email or type(user_email) != str:
            return None
        if not user_pwd or type(user_pwd) != str:
            return None
        user = User.search({'email': user_email})
        if not user or user == []:
            return None
        if user[0].is_valid_password(user_pwd):
            return user[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieve user instance for a request"""
        header_val = self.authorization_header(request)
        extr_val = self.extract_base64_authorization_header(header_val)
        dec_val = self.decode_base64_authorization_header(extr_val)
        user_e, user_p = self.extract_user_credentials(dec_val)
        user = self.user_object_from_credentials(user_e, user_p)
        return user
