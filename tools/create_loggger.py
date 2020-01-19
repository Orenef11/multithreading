import logging
import sys

from colorlog import colorlog

LOGGER_FORMATTER = "%(asctime)s.%(msecs)04d\t[%(threadName)s %(filename)s %(funcName)s %(lineno)d]  " \
                   "%(msecs)d %(name)s [%(levelname)-5.5s] %(message)s"
LOGGER_DATE_TIME_FORMATTER = "%Y-%m-%d %H:%M:%S"


def create_console_logger_handler():
    log = logging.getLogger('')
    log.setLevel(logging.DEBUG)
    log_formatter = logging.Formatter(LOGGER_FORMATTER, LOGGER_DATE_TIME_FORMATTER)
    log_colors = {'DEBUG': 'cyan',
                  'INFO': 'blue',
                  'WARNING': 'yellow',
                  'ERROR': 'red',
                  'CRITICAL': 'white,bg_red'}
    console_formatter = colorlog.ColoredFormatter("%(log_color)s{}".format(
        LOGGER_FORMATTER), datefmt=log_formatter.datefmt, log_colors=log_colors)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    log.addHandler(console_handler)
