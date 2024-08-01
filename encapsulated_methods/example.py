from encapsulated_methods import protected, private


class DecoratedClass:
    @protected
    def _protected_method(self, message):
        print(message)

    @private
    def __private_method(self, message):
        print(message)

    def call_protected_method(self, message):
        self._protected_method(message)

    def call_private_method(self, message):
        self.__private_method(message)


class DecoratedSubclass(DecoratedClass):
    def call_parent_protected_method(self, message):
        self._protected_method(message)

    def call_parent_private_method(self, message):
        self._DecoratedClass__private_method(message)


def main():
    obj = DecoratedClass()
    obj.call_protected_method("Protected method called within the class")
    obj.call_private_method("Private method called within the class\n")
    
    try:
        obj._protected_method("Protected method called outside the class")
    except PermissionError:
        print("Failed to call protected method outside the class")
    try:
        obj._DecoratedClass__private_method("Private method called outside the class")
    except PermissionError:
        print("Failed to call private method outside the class\n")

    obj2 = DecoratedSubclass()
    obj2.call_parent_protected_method("Protected method called from the subclass")
    try:
        obj2.call_parent_private_method("Private method called from the subclass")
    except PermissionError:
        print("Failed to call private method from the subclass")


if __name__ == "__main__":
    main()
