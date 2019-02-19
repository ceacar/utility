import time
def timethis(func, *args):
    """
    this function provides a simple time function which will return func object and time it consumed
    """
    start = time.time()
    func(*args)
    end = time.time()
    return func, end - start
