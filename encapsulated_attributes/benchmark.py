from time import perf_counter
from tabulate import tabulate
from encapsulated_attributes import ProtectedAttribute, PrivateAttribute


class RegularClass:
    def __init__(self):
        self._protected_attr = "Protected"
        self.__private_attr = "Private"

    def get_protected_attribute(self):
        return self._protected_attr

    def set_protected_attribute(self, value):
        self._protected_attr = value

    def get_private_attribute(self):
        return self.__private_attr

    def set_private_attribute(self, value):
        self.__private_attr = value


class RegularSubclass(RegularClass):
    def __init__(self):
        super().__init__()

    def get_protected_attribute(self):
        return self._protected_attr

    def set_protected_attribute(self, value):
        self._protected_attr = value

    def get_private_attribute(self):
        # This will raise an AttributeError
        try:
            return self.__private_attr
        except AttributeError:
            pass

    def set_private_attribute(self, value):
        # This will raise an AttributeError
        try:
            self.__private_attr = value
        except AttributeError:
            pass


class DescriptorClass:
    _protected_attr = ProtectedAttribute()
    __private_attr = PrivateAttribute()

    def __init__(self):
        self._protected_attr = "Protected"
        self.__private_attr = "Private"

    def get_protected_attribute(self):
        return self._protected_attr

    def set_protected_attribute(self, value):
        self._protected_attr = value

    def get_private_attribute(self):
        return self.__private_attr

    def set_private_attribute(self, value):
        self.__private_attr = value


class DescriptorSubclass(DescriptorClass):
    def __init__(self):
        super().__init__()

    def get_protected_attribute(self):
        return self._protected_attr

    def set_protected_attribute(self, value):
        self._protected_attr = value

    def get_private_attribute(self):
        # This will raise a PermissionError
        try:
            return self._DescriptorClass__private_attr
        except PermissionError:
            pass

    def set_private_attribute(self, value):
        # This will raise a PermissionError
        try:
            self._DescriptorClass__private_attr = value
        except PermissionError:
            pass


def benchmark(func, iterations):
    start_time = perf_counter()
    for _ in range(iterations):
        func()
    end_time = perf_counter()
    return end_time - start_time


def main():
    iterations = 1_000_000
    runs = 5

    regular_class = RegularClass()
    regular_subclass = RegularSubclass()
    descriptor_class = DescriptorClass()
    descriptor_subclass = DescriptorSubclass()

    benchmarks = {
        "Get protected": (
            lambda: regular_class.get_protected_attribute(),
            lambda: descriptor_class.get_protected_attribute(),
        ),
        "Set protected": (
            lambda: regular_class.set_protected_attribute("New Protected"),
            lambda: descriptor_class.set_protected_attribute("New Protected"),
        ),
        "Get private": (
            lambda: regular_class.get_private_attribute(),
            lambda: descriptor_class.get_private_attribute(),
        ),
        "Set private": (
            lambda: regular_class.set_private_attribute("New Private"),
            lambda: descriptor_class.set_private_attribute("New Private"),
        ),
        "Get parent protected": (
            lambda: regular_subclass.get_protected_attribute(),
            lambda: descriptor_subclass.get_protected_attribute(),
        ),
        "Set parent protected": (
            lambda: regular_subclass.set_protected_attribute("New Protected"),
            lambda: descriptor_subclass.set_protected_attribute("New Protected"),
        ),
        "Get parent private": (
            lambda: regular_subclass.get_private_attribute(),
            lambda: descriptor_subclass.get_private_attribute(),
        ),
        "Set parent private": (
            lambda: regular_subclass.set_private_attribute("New Private"),
            lambda: descriptor_subclass.set_private_attribute("New Private"),
        ),
    }

    results = {name: {"Regular": [], "Descriptor": []} for name in benchmarks}

    for _ in range(runs):
        for name, (regular_func, descriptor_func) in benchmarks.items():
            results[name]["Regular"].append(benchmark(regular_func, iterations))
            results[name]["Descriptor"].append(benchmark(descriptor_func, iterations))

    table = []
    for name, times in results.items():
        avg_regular = sum(times["Regular"]) / runs
        avg_descriptor = sum(times["Descriptor"]) / runs
        ratio = avg_descriptor / avg_regular
        table.append(
            [
                name,
                f"{avg_regular:.6f}",
                f"{avg_descriptor:.6f}",
                f"{ratio:.2f}",
            ]
        )

    print(f"Benchmark results (average of {runs} runs, {iterations:_} iterations each):")
    print(
        tabulate(
            table,
            headers=[
                "Attribute operation",
                "Regular (s)",
                "Descriptor (s)",
                "Descriptor ÷ Regular",
            ],
        )
    )


if __name__ == "__main__":
    main()
