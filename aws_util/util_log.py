# -*- coding: utf-8 -*-
"""
https://docs.python-guide.org/writing/logging/
https://docs.python.org/3/howto/logging-cookbook.html


my_logger = util_log.logger_setup("my module name", log_file="")
APP_ID    = util_log.create_appid(__file__ )
def log(s1='', s2='', s3='', s4='', s5='', s6='', s7='', s8='', s9='', s10='') :
       my_logger.debug( ",".join( [APP_ID, str(s1), str(s2), str(s3), str(s4), str(s5) ,
                        str(s6), str(s7), str(s8), str(s9), str(s10)] ) )


Attribute name	Format	Description
args	You shouldn’t need to format this yourself.	The tuple of arguments merged into msg to
produce message, or a dict whose values are used for the merge (when there is only one argument,
and it is a dictionary).
asctime	%(asctime)s	Human-readable time when the LogRecord was created. By default this is of
the form ‘2003-07-08 16:49:45,896’ (the numbers after the comma are millisecond portion of the
time).
created	%(created)f	Time when the LogRecord was created (as returned by time.time()).
exc_info	You shouldn’t need to format this yourself.	Exception tuple (à la sys.exc_info)
or, if no exception has occurred, None.
filename	%(filename)s	Filename portion of pathname.
funcName	%(funcName)s	Name of function containing the logging call.
levelname	%(levelname)s	Text logging level for the message ('DEBUG', 'INFO', 'WARNING',
'ERROR', 'CRITICAL').
levelno	%(levelno)s	Numeric logging level for the message (DEBUG, INFO, WARNING, ERROR, CRITICAL).
lineno	%(lineno)d	Source line number where the logging call was issued (if available).
message	%(message)s	The logged message, computed as msg % args. This is set when
Formatter.format() is invoked.
module	%(module)s	Module (name portion of filename).
msecs	%(msecs)d	Millisecond portion of the time when the LogRecord was created.
msg	You shouldn’t need to format this yourself.	The format string passed in the original
logging call. Merged with args to produce message, or an arbitrary object (see Using arbitrary
objects as messages).
name	%(name)s	Name of the logger used to log the call.
pathname	%(pathname)s	Full pathname of the source file where the logging call was issued
(if available).
process	%(process)d	Process ID (if available).
processName	%(processName)s	Process name (if available).
relativeCreated	%(relativeCreated)d	Time in milliseconds when the LogRecord was created,
relative to the time the logging module was loaded.
stack_info	You shouldn’t need to format this yourself.	Stack frame information
(where available) from the bottom of the stack in the current thread, up to and including
the stack frame of the logging call which resulted in the creation of this record.
thread	%(thread)d	Thread ID (if available).
threadName	%(threadName)s	Thread name (if available).




The problem here is that you're not initializing the root logger; you're initializing the logger
for your main module.

Try this for main.py:

import logging
from logging.handlers import RotatingFileHandler
import submodule

logger = logging.getLogger()  # Gets the root logger
logger.setLevel(logging.DEBUG)

fh = RotatingFileHandler('master.log', maxBytes=2000000, backupCount=10)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

logger.debug('DEBUG LEVEL - MAIN MODULE')
logger.info('INFO LEVEL - MAIN MODULE')

submodule.loggerCall()
Then try this for submodule.py:

def loggerCall():
    logger = logging.getLogger(__name__)
    logger.debug('SUBMODULE: DEBUG LOGGING MODE : ')
    logger.info('Submodule: INFO LOG')
    return
Since you said you wanted to send log messages from all your submodules to the same place, you
should initialize the root logger and then simply use the message logging methods
(along with setlevel() calls, as appropriate). Because there's no explicit handler for
your submodule, logging.getLogger(__name__) will traverse the tree to the root,
where it will find the handler you established in main.py.



"""
import logging
import os
import random
import socket
import sys
from logging.handlers import TimedRotatingFileHandler

import arrow

################### Logs #################################################################
APP_ID = __file__ + "," + str(os.getpid()) + "," + str(socket.gethostname())
APP_ID2 = str(os.getpid()) + "_" + str(socket.gethostname())

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logfile.log")
FORMATTER_1 = logging.Formatter("%(asctime)s,  %(name)s, %(levelname)s, %(message)s")
FORMATTER_2 = logging.Formatter("%(asctime)s.%(msecs)03dZ %(levelname)s %(message)s")
FORMATTER_3 = logging.Formatter("%(asctime)s  %(levelname)s %(message)s")
FORMATTER_4 = logging.Formatter("%(asctime)s, %(process)d, %(filename)s,    %(message)s")


FORMATTER_5 = logging.Formatter(
    "%(asctime)s, %(process)d, %(pathname)s%(filename)s, %(funcName)s, %(lineno)s,  %(message)s"
)


# LOG_FILE = "my_app.log"


#########################################################################################
def create_appid(filename):
    # appid  = filename + ',' + str(os.getpid()) + ',' + str( socket.gethostname() )
    appid = filename + "," + str(os.getpid())
    return appid


def create_logfilename(filename):
    return filename.split("/")[-1].split(".")[0] + ".log"


def create_uniqueid():
    return arrow.utcnow().to("Japan").format("_YYYYMMDDHHmmss_") + str(random.randint(1000, 9999))


########################################################################################
################### Logger #############################################################
def logger_setup(
    logger_name=None,
    log_file=None,
    formatter=FORMATTER_1,
    isrotate=False,
    isconsole_output=True,
    logging_level=logging.DEBUG,
):
    """
    my_logger = util_log.logger_setup("my module name", log_file="")
    APP_ID    = util_log.create_appid(__file__ )
    def log(*argv):
      my_logger.info(",".join([str(x) for x in argv]))
  
   """

    if logger_name is None:
        logger = logging.getLogger()  # Gets the root logger
    else:
        logger = logging.getLogger(logger_name)

    logger.setLevel(logging_level)  # better to have too much log than not enough

    if isconsole_output:
        logger.addHandler(logger_handler_console(formatter))

    if log_file is not None:
        logger.addHandler(
            logger_handler_file(formatter=formatter, log_file_used=log_file, isrotate=isrotate)
        )

    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger


def logger_handler_console(formatter=None):
    formatter = FORMATTER_1 if formatter is None else formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    return console_handler


def logger_handler_file(isrotate=False, rotate_time="midnight", formatter=None, log_file_used=None):
    formatter = FORMATTER_1 if formatter is None else formatter
    log_file_used = LOG_FILE if log_file_used is None else log_file_used
    if isrotate:
        print("Rotate log", rotate_time)
        fh = TimedRotatingFileHandler(log_file_used, when=rotate_time)
        fh.setFormatter(formatter)
        return fh
    else:
        fh = logging.FileHandler(log_file_used)
        fh.setFormatter(formatter)
        return fh


def logger_setup2(name=__name__, level=None):
    _ = level

    # logger defines
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


##########################################################################################
################### Print ################################################################
def printlog(
    s="",
    s1="",
    s2="",
    s3="",
    s4="",
    s5="",
    s6="",
    s7="",
    s8="",
    s9="",
    s10="",
    app_id="",
    logfile=None,
    iswritelog=True,
):
    try:
        if app_id != "":
            prefix = app_id + "," + arrow.utcnow().to("Japan").format("YYYYMMDD_HHmmss,")
        else:
            prefix = APP_ID + "," + arrow.utcnow().to("Japan").format("YYYYMMDD_HHmmss,")
        s = ",".join(
            [
                prefix,
                str(s),
                str(s1),
                str(s2),
                str(s3),
                str(s4),
                str(s5),
                str(s6),
                str(s7),
                str(s8),
                str(s9),
                str(s10),
            ]
        )

        print(s)
        if writelog:
            writelog(s, logfile)
    except Exception as e:
        print(e)
        if iswritelog:
            writelog(str(e), logfile)


def writelog(m="", f=None):
    f = LOG_FILE if f is None else f
    with open(f, "a") as _log:
        _log.write(m + "\n")
