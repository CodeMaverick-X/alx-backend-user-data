#!/usr/bin/env python
"""
contains view for session authentication
"""
from flask import jsonify, make_response, request
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_Session():
    """handles authentication for session"""

    email = request.form.get('email')
    password = request.form.get('password')

    if not email or email == "":
        return jsonify({"error": "email missing"}), 400
    if not password or password == "":
        return jsonify({"error": "password missing"}), 400

    user_l = User.search({'email': email})
    if user_l == [] or not user_l:
        return jsonify({"error": "no user found for this email"}), 400

    user = user_l[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth

    sess_id = auth.create_session(user.id)
    sess_name = getenv('SESSION_NAME')
    resp = make_response(jsonify(user.to_json()))
    resp.set_cookie(sess_name, sess_id)
    return resp
