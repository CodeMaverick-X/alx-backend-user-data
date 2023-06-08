#!/usr/bin/env python3
"""
conatins flask app"""
from flask import Flask, jsonify, request, abort,\
                  make_response, redirect, url_for
from user import User
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index():
    """return a json message"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
    """register mnew user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        if user is None:
            raise ValueError
    except (ValueError):
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": user.email, "message": "user created"})


@app.route('/sessions', methods=['POST'])
def login():
    """login and create session"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    sess_id = AUTH.create_session(email)
    resp = make_response(jsonify({"email": "{}".format(email),
                                  "message": "logged in"}))
    resp.set_cookie('session_id', sess_id)
    return resp


@app.route('/sessions', methods=['DELETE'])
def logout():
    """log out and delete session id"""
    sess_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(sess_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('index'))


@app.route('/profile', methods=['GET'])
def profile():
    """return the user profile(email) based on sess_id"""
    sess_id = request.cookies.get('session_id')
    if not sess_id or sess_id == "":
        abort(403)
    user = AUTH.get_user_from_session_id(sess_id)
    if not user:
        abort(403)
    return jsonify({"email": "{}".format(user.email)})


@app.route('/reset_password', methods=['POST'])
def reset_password():
    """reset user password"""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
    except (ValueError):
        abort(403)
    else:
        return jsonify({"email": email, "reset_token": token}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
