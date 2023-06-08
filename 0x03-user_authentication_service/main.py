#!/usr/bin/env python3
"""
Main file
for intigreation test
"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str):
    """Test register user endpoint"""
    response = requests.post(
        f"{BASE_URL}/users",
        {'email': email, 'password': password}).json()
    expected = {
        'email': 'guillaume@holberton.io', 'message': 'user created'}
    assert response == expected


def log_in_wrong_password(email: str, password: str):
    """Test wrong user login"""
    response = requests.post(
        f"{BASE_URL}/sessions",
        {'email': email, 'password': password})
    assert response.status_code == 401


def profile_unlogged():
    """Test not logged in user"""
    response = requests.get(f"{BASE_URL}/profile",
                            cookies={'session_id': 'nope'})
    assert response.status_code == 403


def log_in(email: str, password: str):
    """Test login user endpoint"""
    response = requests.post(
        f"{BASE_URL}/sessions",
        {'email': email, 'password': password})
    if response.status_code == 200:
        expected = {'email': 'guillaume@holberton.io', 'message': 'logged in'}
        assert response.json() == expected
        return response.cookies.get("session_id")


def profile_logged(session_id: str):
    """Test logged in user endpoint"""
    response = requests.get(f"{BASE_URL}/profile",
                            cookies={'session_id': session_id})
    expected = {'email': 'guillaume@holberton.io'}
    assert response.json() == expected


def log_out(session_id):
    """Test logout user endpoint"""
    response = requests.delete(f"{BASE_URL}/sessions",
                               cookies={'session_id': session_id})
    expected = {'message': 'Bienvenue'}
    assert response.json() == expected


def reset_password_token(email: str):
    """Test reset password endpoint"""
    response = requests.post(f"{BASE_URL}/reset_password",
                             {'email': email})
    data = response.json()
    assert type(data.get("reset_token")) == str
    assert data.get("email") == email
    return data.get("reset_token")


def update_password(email: str, reset_token: str, new_password: str):
    """Test update password"""
    response = requests.put(f"{BASE_URL}/reset_password",
                            {'email': email,
                             'reset_token': reset_token,
                             'new_password': new_password})
    data = response.json()
    expected = {"email": f"{email}", "message": "Password updated"}
    assert data == expected


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)