#!/usr/bin/env python3
"""
contains a function called filter_datum that
returns the log message obfuscated
"""
from typing import List
import re
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
