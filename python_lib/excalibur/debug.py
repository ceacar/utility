import sys
def debug(func):
    def wrap(*args, **kwargs):
        sys.stderr.write(
            ">{func_name} with args:{ag}, kwargs:{kg}"\
            .format(
                func_name = func.__qualname__,
                ag = *args, kg = **kwargs
            )
        )
        func(*args, **kwargs)
    return wrap
