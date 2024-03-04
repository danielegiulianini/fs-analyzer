from typing import Callable


def call_if_not_none_with_param[T](function: Callable[[T], None], param: T):
    if function is not None:
            function(param)