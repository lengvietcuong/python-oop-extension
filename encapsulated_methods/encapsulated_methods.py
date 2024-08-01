import inspect


def protected(func):
    def wrapper(*args, **kwargs):
        frame = inspect.currentframe().f_back  # Get the frame info of the caller
        if "self" in frame.f_locals:
            defining_class_name = func.__qualname__.split(".")[0]
            defining_class = getattr(
                inspect.getmodule(func), defining_class_name, None
            )
            # Check if 'self' is an instance of the defining class or its subclasses
            if defining_class and isinstance(
                frame.f_locals["self"], defining_class
            ):
                return func(*args, **kwargs)

        raise PermissionError(
            f"Protected function '{func.__name__}' cannot be called outside its defining class and subclasses"
        )

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


def private(func):
    def wrapper(*args, **kwargs):
        frame = inspect.currentframe().f_back  # Get the frame info of the caller
        if "self" in frame.f_locals:
            defining_class_name = func.__qualname__.split(".")[0]
            defining_class = getattr(
                inspect.getmodule(func), defining_class_name, None
            )
            # Check if 'self' is an instance of the defining class
            if type(frame.f_locals["self"]) == defining_class:
                return func(*args, **kwargs)

        raise PermissionError(
            f"Private function '{func.__name__}' cannot be called outside it defining class"
        )

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper
