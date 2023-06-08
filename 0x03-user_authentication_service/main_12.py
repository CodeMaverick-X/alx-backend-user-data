#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)

sess = auth.create_session(email)
print(sess)
user = auth.get_user_from_session_id(sess)
print(user)
if user:
    print(user.session_id)