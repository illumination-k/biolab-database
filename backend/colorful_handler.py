import logging

mapping = {
    "TRACE": "[ trace ]",
    "DEBUG": "[ \x1b[0;36mdebug\x1b[0m ]",
    "INFO": "[ \x1b[0;32minfo\x1b[0m ]",
    "WARNING": "[ \x1b[0;33mwarn\x1b[0m ]",
    "WARN": "[ \x1b[0;33mwarn\x1b[0m ]",
    "ERROR": "\x1b[0;31m[ error ]\x1b[0m",
    "ALERT": "\x1b[0;37;41m[ alert ]\x1b[0m",
    "CRITICAL": "\x1b[0;37;41m[ alert ]\x1b[0m",
}


class ColorfulHandler(logging.StreamHandler):
    def emit(self, record):
        record.levelname = mapping[record.levelname]
        super().emit(record)
