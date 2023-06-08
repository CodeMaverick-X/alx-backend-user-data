#!/usr/bin/env python3
"""
conatins flask app"""
from flask import Flask, jsonify, request, abort, make_response
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
