"""Decorators
>>> @report

"""

import logging
import time
import sys
import resource
from functools import wraps, partial

# TODO: put this inside the decorators?
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Number of times to indent the output
# Using a list rather than an int will make it faster by forcing it to be a reference
__debug_report_indent = [0]

__debug_time_indent = [0]
__debug_time_t0 = time.time()


def debug_report(wrapped_function=None, prefix='', max_arg_len=40):
    """Log the occurence of execution start and return for `wrapped_function` with indentation for trace depth.

    Usage:
        >>> # Wrap a function normally with debug_report which causes wrapped_func to print out debug messages each time it is called
        >>> @debug_report
        >>> def doubleit(num):
        >>>    return num * 2
        >>> doubleit(5)
        10

        # this will wrap the function as before but use the prefix argument to append a string to the beginning of the debug messages
        >>> # Wrap a function normally with debug_report which causes wrapped_func to print out debug messages each time it is called
        >>> @debug_report(prefix='Hello world: ')
        >>> def doubleit(num):
        >>>    return num * 2
        >>> doubleit(4)
        10


    """

    # If the user has not passed any arguments then return the function wrapper function,
    #  but don't specify any default argument so the wrapped_function can be passed in as the sole argument
    if wrapped_function in [None, False]:
        # return the 
        return partial(debug_report, prefix=prefix)

    @wraps(wrapped_function)
    def wrap(*args, **kwargs):
        N_calls = wrap.callcount = wrap.callcount + 1

        indent = '  ' * __debug_report_indent[0]
        list_argdefs = [repr(arg) for arg in args] + ["%s=%s" % (kwd, repr(arg)) for kwd, arg in kwargs.items()]
        call_string = "%s(%s)" % (wrapped_function.__name__, ', '.join(list_argdefs))  # use __qualname__ in python 3
        if len(call_string) > max_arg_len:
            call_string = call_string[:max_arg_len] + '...)'
        msg = prefix + "--> %s%s [%06d]" % (indent, call_string, N_calls)
        # sys.stderr.write(msg + '\n')
        logger.debug(msg)
        __debug_report_indent[0] = __debug_report_indent[0] + 1
        retval = wrapped_function(*args, **kwargs)
        __debug_report_indent[0] = __debug_report_indent[0] - 1
        msg = "<-- %s%s = %s [%06d]" % (indent, repr(retval), call_string, N_calls)
        logger.debug(msg)

        return retval
    wrap.callcount = 0

    return wrap


def debug_time(wrapped_function, max_arg_len=40):
    """Time the execution of wrapped_function and log the execution time with indentation for trace depth."""

    @wraps(wrapped_function)
    def wrap(*args, **kwargs):
        N_calls = wrap.callcount = wrap.callcount + 1

        indent = '  ' * __debug_report_indent[0]
        list_argdefs = [repr(arg) for arg in args] + ["%s=%s" % (kwd, repr(arg)) for kwd, arg in kwargs.items()]
        call_string = "%s(%s)" % (wrapped_function.__name__, ', '.join(list_argdefs))
        if len(call_string) > max_arg_len:
            call_string = call_string[:max_arg_len] + '...)'
        msg = "--> %s%s [%06d]" % (indent, call_string, N_calls)
        # sys.stderr.write(msg + '\n')
        logger.debug(msg)
        __debug_report_indent[0] = __debug_report_indent[0] + 1
        t0 = time.time()
        retval = wrapped_function(*args, **kwargs)
        t1 = time.time()
        __debug_report_indent[0] = __debug_report_indent[0] - 1
        msg = "<-- %s%s [%06d, %010.3f ms]" % (indent, call_string, N_calls, (t1 - t0) * 1000.)
        sys.stderr.write(msg + '\n')
        logger.debug(msg)

        return retval
    wrap.callcount = 0
    #wrap.__name__ = 'wrapped<' + wrapped_function.__name__ + '>'

    return wrap


def debug_mem(wrapped_function, max_arg_len=40):
    """Time the execution of wrapped_function and log the execution time with indentation for trace depth."""

    @wraps(wrapped_function)
    def wrap(*args, **kwargs):
        N_calls = wrap.callcount = wrap.callcount + 1

        indent = '  ' * __debug_report_indent[0]
        list_argdefs = [repr(arg) for arg in args] + ["%s=%s" % (kwd, repr(arg)) for kwd, arg in kwargs.items()]
        call_string = "%s(%s)" % (wrapped_function.__name__, ', '.join(list_argdefs))
        if len(call_string) > max_arg_len:
            call_string = call_string[:max_arg_len] + '...)'
        msg = "--> %s%s [%06d]" % (indent, call_string, N_calls)
        # sys.stderr.write(msg + '\n')
        logger.debug(msg)
        __debug_report_indent[0] = __debug_report_indent[0] + 1
        m0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        retval = wrapped_function(*args, **kwargs)
        m1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        __debug_report_indent[0] = __debug_report_indent[0] - 1
        msg = "<-- %s%s [%06d, %010.3f kB]" % (indent, call_string, N_calls, (m1 - m0) / 1000.)
        sys.stderr.write(msg + '\n')
        logger.debug(msg)

        return retval
    wrap.callcount = 0
    #wrap.__name__ = 'wrapped<' + wrapped_function.__name__ + '>'

    return wrap
