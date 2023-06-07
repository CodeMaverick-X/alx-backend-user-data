#!/usr/bin/env python3
"""contains a fincion that hashes pass with bcrypt"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """hash user password"""
    bytes_s = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_p = bcrypt.hashpw(bytes_s, salt)
    return hash_p
