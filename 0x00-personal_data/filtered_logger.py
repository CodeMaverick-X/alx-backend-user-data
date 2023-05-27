#!/usr/bin/env python3
"""
contains a function called filter_datum that
returns the log message obfuscated
"""
from typing import List, Dict
from mysql.connector import MySQLConnection
import mysql.connector
import re
import os
import logging
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """redact document like i'm in the FBI ;)"""
    for field in fields:
        message = re.sub(rf'{field}=(\w+|.+?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format the redacted str"""
        r_message = filter_datum(self.fields, self.REDACTION,
                                 record.getMessage(), self.SEPARATOR)
        record.msg = r_message
        return super().format(record)


def get_logger() -> logging.Logger:
    """returns a Logger"""
    logger = logging.getLogger("user_data")
    logger.propagate = False
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> MySQLConnection:
    """returns db connection"""
    return mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD"),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )


def main():
    """Entry Point"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT name, email, phone, ssn, password, last_login,\
        user_agent FROM users;")
    logger = get_logger()
    for row in cursor:
        logger.info("name={};email={};phone={};ssn={};password={};\
                    last_login={};user_agent={};".
                    format(row[0], row[1], row[2], row[3], row[4],
                           row[5], row[6]))
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
