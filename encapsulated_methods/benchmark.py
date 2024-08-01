from time import perf_counter
from tabulate import tabulate
from encapsulated_methods import protected, private


class RegularClass:
    def __init__(self):
        pass

    def _protected_method(self):
        pass

    def __private_method(self):
        pass

    def call_protected_method(self):
        self._protected_method()

    def call_private_method(self):
        self.__private_method()


class RegularSubclass(RegularClass):
    def call_parent_protected_method(self):
        self._protected_method()

    def call_parent_private_method(self):
        # This will raise an AttributeError
        try:
            self.__private_method()
        except AttributeError:
            pass


class DecoratedClass:
    @protected
    def _protected_method(self):
        pass

    @private
    def __private_method(self):
        pass

    def call_protected_method(self):
        self._protected_method()

    def call_private_method(self):
        self.__private_method()


class DecoratedSubclass(DecoratedClass):
    def call_parent_protected_method(self):
        self._protected_method()

    def call_parent_private_method(self):
        # This will raise a PermissionError
        try:
            self._DecoratedClass__private_method()
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
    decorated_class = DecoratedClass()
    decorated_subclass = DecoratedSubclass()

    benchmarks = {
        "Protected": (
            lambda: regular_class.call_protected_method(),
            lambda: decorated_class.call_protected_method(),
        ),
        "Private": (
            lambda: regular_class.call_private_method(),
            lambda: decorated_class.call_private_method(),
        ),
        "Parent's protected": (
            lambda: regular_subclass.call_parent_protected_method(),
            lambda: decorated_subclass.call_parent_protected_method(),
        ),
        "Parent's private": (
            lambda: regular_subclass.call_parent_private_method(),
            lambda: decorated_subclass.call_parent_private_method(),
        ),
    }

    results = {name: {"Regular": [], "Decorated": []} for name in benchmarks}

    for _ in range(runs):
        for name, (regular_func, decorated_func) in benchmarks.items():
            results[name]["Regular"].append(benchmark(regular_func, iterations))
            results[name]["Decorated"].append(benchmark(decorated_func, iterations))

    table = []
    for name, times in results.items():
        avg_regular = sum(times["Regular"]) / runs
        avg_decorated = sum(times["Decorated"]) / runs
        ratio = avg_decorated / avg_regular
        table.append(
            [
                name,
                f"{avg_regular:.6f}",
                f"{avg_decorated:.6f}",
                f"{ratio:.2f}",
            ]
        )

    print(
        f"Benchmark results (average of {runs} runs, {iterations:_} iterations each):"
    )
    print(
        tabulate(
            table,
            headers=[
                "Method call",
                "Regular (s)",
                "Decorated (s)",
                "Decorated ÷ Regular",
            ],
        )
    )


if __name__ == "__main__":
    main()
