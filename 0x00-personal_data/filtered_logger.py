#!/usr/bin/env python3
"""
contains a function called filter_datum that
returns the log message obfuscated
"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """redact document like i'm in the FBI ;)"""
    for field in fields:
        message = re.sub(r'{}=(\w+|\d+\/\d+\/\d+){}'.format(field, separator),
                         '{}={}{}'.format(field, redaction, separator), message)
    return message
