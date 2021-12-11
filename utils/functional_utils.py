from typing import Callable, Any

from utils.generic_utils import T, V


def curry(func: Callable[..., T], arg_count=None) -> Callable[..., T]:
    arg_count = arg_count if arg_count is not None else func.__code__.co_argcount

    def partial_func(*args):
        if len(args) == arg_count:
            return func(*args)

        def inner_partial_func(*rest_args):
            return func(*(args + rest_args))

        return curry(inner_partial_func, arg_count - len(args))

    return partial_func


@curry
def apply_to_result(decorator: Callable[[T], V], func: Callable[..., T], *args: Any) -> Callable[..., V]:
    return decorator(func(*args))
