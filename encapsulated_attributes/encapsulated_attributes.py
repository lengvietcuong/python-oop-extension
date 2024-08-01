import inspect


class ProtectedAttribute:
    def __set_name__(self, owner, name):
        self.name = name
        self.defining_class = owner

    def __get__(self, instance, owner=None):
        frame = inspect.currentframe().f_back  # Get the frame info of the caller
        if "self" in frame.f_locals:
            # Check if 'self' is an instance of the defining class
            if isinstance(frame.f_locals["self"], self.defining_class):
                return instance.__dict__[self.name]

        raise PermissionError(
            f"Protected attribute '{self.name}' cannot be accessed outside its defining class or subclasses"
        )

    def __set__(self, instance, value):
        frame = inspect.currentframe().f_back  # Get the frame info of the caller
        if "self" in frame.f_locals:
            # Check if 'self' is an instance of the defining class
            if isinstance(frame.f_locals["self"], self.defining_class):
                instance.__dict__[self.name] = value
                return

        raise PermissionError(
            f"Protected attribute '{self.name}' cannot be set outside its defining class or subclasses"
        )


class PrivateAttribute:
    def __set_name__(self, owner, name):
        self.name = name
        self.defining_class = owner
        
    def __get__(self, instance, owner=None):
        frame = inspect.currentframe().f_back  # Get the frame info of the caller
        if "self" in frame.f_locals:
            # Check if 'self' is an instance of the defining class
            if type(frame.f_locals["self"]) == self.defining_class:
                return instance.__dict__[self.name]

        raise PermissionError(
            f"Private attribute '{self.name}' cannot be accessed outside its defining class"
        )

    def __set__(self, instance, value):
        frame = inspect.currentframe().f_back  # Get the frame info of the caller
        if "self" in frame.f_locals:
            # Check if 'self' is an instance of the defining class
            if type(frame.f_locals["self"]) == self.defining_class:
                instance.__dict__[self.name] = value
                return
            elif (
                isinstance(frame.f_locals["self"], self.defining_class)
                and frame.f_code.co_name == "__init__"
            ):
                return  # Do nothing if called from __init__ of a subclass

        raise PermissionError(
            f"Private attribute '{self.name}' cannot be set outside its defining class"
        )
