#!/usr/bin/env python3
"""
Module for handling Personal Data
"""
import re
from typing import List
import logging
from os import environ
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Obfuscates specified fields in a message.

    Arguments:
    fields -- List of field names that should be obfuscated.
    redaction -- The value that should replace the obfuscated fields.
    message -- The message that contains the fields.
    separator -- The character that separates fields in the message.

    Returns:
    The message with the specified fields obfuscated.
    """
    for f in fields:
        message = re.sub(f"{f}=.*?{separator}",
                         f"{f}={redaction}{separator}", message)
    return message


def get_logger() -> logging.Logger:
    """
    Creates and returns a logger object with specific settings.

    The logger object is named "user_data" and its level is set to INFO.
    Propagation is turned off to prevent the log messages from being passed
    to the root logger. A stream handler with a specific formatter is added
    to the logger. This formatter obfuscates fields defined in PII_FIELDS.

    Returns:
        logging.Logger: The configured logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establishes a connection to a MySQL database.

    Uses the following environment variables for the database credentials:
    - PERSONAL_DATA_DB_USERNAME: The username for the database
      (default is "root").
    - PERSONAL_DATA_DB_PASSWORD: The password for the database
      (default is an empty string).
    - PERSONAL_DATA_DB_HOST: The host of the database
      (default is "localhost").
    - PERSONAL_DATA_DB_NAME: The name of the database.

    Returns:
        A MySQLConnection object representing the established
          database connection.
    """
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    db = mysql.connector.connection.MySQLConnection(user=username,
                                                    password=password,
                                                    host=host,
                                                    database=db_name)
    return db


def main():
    """
    Retrieves all rows in the 'users' table of the database and logs each row.

    The log message is formatted by a RedactingFormatter to obfuscate
      fields defined in PII_FIELDS.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    fields = ["name", "email", "phone", "ssn", "password"]
    formatter = RedactingFormatter(fields)

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    for row in cursor:
        message = ";".join(f"{f}={v}" for f, v in zip(fields, row))
        log_record = logging.LogRecord("user_data", logging.INFO,
                                       None, None, message, None, None)
        print(formatter.format(log_record))

    cursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records using filter_datum"""
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR
        )
        return super(RedactingFormatter, self).format(record)


if __name__ == "__main__":
    main()
