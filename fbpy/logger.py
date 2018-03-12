DEBUG=1
INFO=2
WARNING=3
ERROR=4

LogLevel = DEBUG


import sys
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

def _sanitize(msg):
    return msg.translate(non_bmp_map)

def debug(msg):
    msg=_sanitize(msg)
    if LogLevel <= DEBUG:
        print(msg)

def info(msg):
    msg=_sanitize(msg)
    if LogLevel <= INFO:
        print(msg)

def warning(msg):
    msg=_sanitize(msg)
    if LogLevel <= WARNING:
        print(msg)

def error(msg):
    msg=_sanitize(msg)
    if LogLevel <= ERROR:
        print(msg)
