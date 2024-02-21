#!/usr/bin/env python3
""" DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User
from typing import TypeVar

VALID_FIELDS = ["id", "email", "hashed_password", "session_id", "reset_token"]


class DB:
    """
    DB class.
    """

    def __init__(self):
        """
        Constructor.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """
        _session.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a user instance to the session DB

        Parameters:
        email (str): The email of the user to be added.
        hashed_password (str): The hashed password of the user to be added.

        Returns:
        User: The added user object.
        """
        if not email or not hashed_password:
            return
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database by using keyword arguments.

        Parameters:
        **kwargs: Variable length keyword arguments used for searching
          the user.

        Returns:
        User: The user object if found.

        Raises:
        InvalidRequestError: If no arguments or invalid fields are provided.
        NoResultFound: If no user is found.
        """
        if not kwargs or any(x not in VALID_FIELDS for x in kwargs):
            raise InvalidRequestError
        session = self._session
        try:
            return session.query(User).filter_by(**kwargs).one()
        except Exception as exc:
            raise NoResultFound from exc

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's fields in the database.

        Parameters:
        user_id (int): The id of the user to be updated.
        **kwargs: Variable length keyword arguments used for updating
          the user's fields.

        Raises:
        ValueError: If invalid fields are provided.
        """
        session = self._session
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if k not in VALID_FIELDS:
                raise ValueError
            setattr(user, k, v)
        session.commit()
