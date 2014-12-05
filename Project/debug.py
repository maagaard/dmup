__author__ = "Emil Maagaard & Bjarke Vad Andersen"
__credits__ = []
__version__ = "1.0"

# Debug defines
DEBUG = True


def DLOG(log_message):
    """
    Debug log.
    Print log message when debugging.
    """
    if DEBUG:
        print log_message
