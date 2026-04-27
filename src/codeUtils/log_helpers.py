"""
Created on Mon April 27 21:14:42 2026

@author: ndagg
"""

import logging

class MyFormatter(logging.Formatter):
    def __init__(self, fmt):
        logging.Formatter.__init__(self, fmt)
        self.indent = 0

    def format(self, record):
        indent = self.indent * "     "
        msg = logging.Formatter.format(self, record)

        msg = msg.replace("mainlogger.", "")
        preamble, msg = msg.split("-")
        preamble = preamble + " " * (20 - len(preamble))
        msg = preamble + indent + "-" + msg

        return msg
    

# Clear log file
with open("main_log.txt", "w") as file:
    file.write("")

logger = logging.getLogger("mainlogger")
logger.setLevel(logging.DEBUG)

# Create file handler
handler = logging.FileHandler("main_log.txt")
handler.setLevel(logging.DEBUG)

# Create formatter with desired format
formatter = MyFormatter('%(levelname)s::%(name)s - %(message)s')
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)