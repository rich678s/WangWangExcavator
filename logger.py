#--* coding=utf-8 *--
import logging

# define logger
logger = logging.getLogger(u"Excavator")
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)