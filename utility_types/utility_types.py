from dataclasses import field, fields, make_dataclass
import inspect


def pick(new_class_name, base_class, fields_to_pick):
    """Creates a new dataclass from a given dataclass with only the specified fields."""
    new_class_fields = [
        (base_class_field.name, base_class_field.type)
        for base_class_field in fields(base_class)
        if base_class_field.name in fields_to_pick
    ]
    new_class = make_dataclass(new_class_name, new_class_fields)

    return new_class


def omit(new_class_name, base_class, fields_to_omit):
    """Creates a new dataclass from a given dataclass with certain fields omitted."""
    new_class_fields = [
        (base_class_field.name, base_class_field.type)
        for base_class_field in fields(base_class)
        if base_class_field.name not in fields_to_omit
    ]
    new_class = make_dataclass(new_class_name, new_class_fields)
    _copy_methods(new_class, base_class)

    return new_class


def partial(new_class_name, base_class):
    """Creates a new dataclass from a given dataclass with all fields optional."""
    new_class_fields = [
        (base_class_field.name, base_class_field.type, field(default=None))
        for base_class_field in fields(base_class)
    ]
    new_class = make_dataclass(new_class_name, new_class_fields)
    _copy_methods(new_class, base_class)

    return new_class


def required(new_class_name, base_class):
    """Creates a new dataclass from a given dataclass with all fields required."""
    new_class_fields = [
        (base_class_field.name, base_class_field.type, field())
        for base_class_field in fields(base_class)
    ]
    new_class = make_dataclass(new_class_name, new_class_fields)
    _copy_methods(new_class, base_class)

    return new_class


def _copy_methods(new_class, base_class):
    for method_name, value in inspect.getmembers(
        base_class, predicate=inspect.isroutine
    ):
        if method_name not in new_class.__dict__:  # Only copy if not already defined
            setattr(new_class, method_name, value)
