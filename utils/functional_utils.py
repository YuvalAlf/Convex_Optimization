from typing import Callable, Any, Union

from utils.generic_utils import T, V


def force_curry(func: Callable[..., T]) -> Callable[..., Callable[..., T]]:
    def inner1(*args1: Any, **kwargs1: Any) -> Callable[..., T]:
        def inner2(*args2: Any, **kwargs2: Any) -> T:
            return func(*(args1 + args2), **{**kwargs1, **kwargs2})

        return inner2

    return inner1


@force_curry
@force_curry
def apply_to_result(decorator: Callable[[T], V], func: Callable[..., T], *args: Any) -> Callable[..., V]:
    return decorator(func(*args))


# noinspection PyBroadException
@force_curry
@force_curry
def on_error_return(on_error_value: V, func: Callable[..., T], *args: Any, **kwargs: Any) -> Union[V, T]:
    try:
        return func(*args, **kwargs)
    except Exception as _:
        return on_error_value


def run_if(value: bool, func: Callable[[], None]):
    if value:
        func()
