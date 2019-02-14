import time
import sys
from functools import wraps
def timeit(orig_func):
    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = orig_func(*args, **kwargs)
        end = time.time()
        sys.stderr.write("took {0} seconds to finish {1}".format(end - start, orig_func.__name__))
        return res

    return wrapper




