# Debug defines
DEBUG = True


def DLOG(log_message):
    """
    Debug log.
    Print log message when debugging.
    """
    if DEBUG:
        print log_message
