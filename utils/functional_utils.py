
def apply_to_result(decorator):
    def function(func):
        def inner(*args, **kwargs):
            return decorator(func(*args, **kwargs))
        return inner
    return function

