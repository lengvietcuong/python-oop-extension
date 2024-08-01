from encapsulated_attributes import ProtectedAttribute, PrivateAttribute


class DescriptorClass:
    _protected_attribute = ProtectedAttribute()
    __private_attribute = PrivateAttribute()

    def __init__(self):
        self._protected_attribute = "Protected value"
        self.__private_attribute = "Private value"

    def get_protected_attribute(self):
        return self._protected_attribute

    def get_private_attribute(self):
        return self.__private_attribute

    def set_protected_attribute(self, value):
        self._protected_attribute = value

    def set_private_attribute(self, value):
        self.__private_attribute = value


class DescriptorSubclass(DescriptorClass):
    def __init__(self):
        super().__init__()

    def get_parent_protected_attribute(self):
        return self._protected_attribute

    def get_parent_private_attribute(self):
        return self._DescriptorClass__private_attribute

    def set_parent_protected_attribute(self, value):
        self._protected_attribute = value

    def set_parent_private_attribute(self, value):
        self._DescriptorClass__private_attribute = value


def main():
    obj = DescriptorClass()
    print(f"Get protected attribute within the class: {obj.get_protected_attribute()}")
    print(f"Get private attribute within the class: {obj.get_private_attribute()}\n")
    try:
        print(f"Get protected attribute outside the class: {obj._protected_attribute}")
    except PermissionError:
        print("Failed to get protected attribute outside the class")
    try:
        print(
            f"Get private attribute outside the class: {obj._DescriptorClass__private_attribute}"
        )
    except PermissionError:
        print("Failed to get private attribute outside the class\n")

    obj.set_protected_attribute("New protected value")
    obj.set_private_attribute("New private value")
    print(f"Set protected attribute within the class: {obj.get_protected_attribute()}")
    print(f"Set private attribute within the class: {obj.get_private_attribute()}\n")

    obj2 = DescriptorSubclass()
    print(
        f"Get parent protected attribute from the subclass: {obj2.get_parent_protected_attribute()}"
    )
    try:
        print(
            f"Get parent private attribute from the subclass: {obj2.get_parent_private_attribute()}"
        )
    except PermissionError:
        print("Failed to get parent private attribute from the subclass\n")

    obj2.set_parent_protected_attribute("New parent protected value")
    print(
        f"Set parent protected attribute from the subclass: {obj2.get_parent_protected_attribute()}"
    )


if __name__ == "__main__":
    main()
