from typing import Callable, Any, Union

from utils.generic_utils import T, V


def regular_curry(func: Callable[..., T], arg_count=None) -> Callable[..., T]:
    arg_count = arg_count if arg_count is not None else func.__code__.co_argcount

    def partial_func(*args):
        if len(args) == arg_count:
            return func(*args)

        def inner_partial_func(*rest_args):
            return func(*(args + rest_args))

        return regular_curry(inner_partial_func, arg_count - len(args))

    return partial_func


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


@on_error_return(7)
def f(num):
    return float(num)


class cached_property:
    def __init__(self, factory):
        self._attr_name = factory.__name__
        self._factory = factory

    def __get__(self, instance, owner):
        attr = self._factory(instance)

        setattr(instance, self._attr_name, attr)

        return attr
