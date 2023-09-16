import logging
import traceback


def exception_hook(exception_type, exception_value, exception_tb):
    """
    Intended to be assigned to sys.exception as a hook.
    Gives programmer opportunity to do something useful with info
    from uncaught exceptions.

    Parameters
    type: Exception type
    value: Exception's value
    tb: Exception's traceback
    """

    logging.error("an error have been declared:" +
                  "\n" + " "*34 + "Type of error: " + exception_type.__name__ +
                  "\n" + " "*34 + str(exception_value) +
                  "\n" + " "*32 + str(
                      traceback.format_tb(exception_tb)[-1].split("\n")[0]))
