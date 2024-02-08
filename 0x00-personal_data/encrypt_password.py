#!/usr/bin/env python3
"""
Encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password with bcrypt.

    Arguments:
    password -- The password to hash.

    Returns:
    A byte string representing the hashed password.
    """
    encoded = password.encode()
    hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks if a provided password matches the hashed password.

    Arguments:
    hashed_password -- The hashed password.
    password -- The password to check.

    Returns:
    True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
