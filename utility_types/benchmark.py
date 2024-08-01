from time import perf_counter
from dataclasses import dataclass, make_dataclass
from typing import Optional
from tabulate import tabulate
from utility_types import omit, pick, partial, required


# Define an arbitrary base class
@dataclass
class BaseClass:
    field1: int
    field2: str
    field3: float
    field4: bool
    field5: str


# Manually copied classes (Regular approach)
def create_omitted_class_regular():
    @dataclass
    class OmittedClassRegular:
        field1: int
        field3: float
        field5: Optional[str] = None

    return OmittedClassRegular


def create_picked_class_regular():
    @dataclass
    class PickedClassRegular:
        field2: str
        field4: bool

    return PickedClassRegular


def create_partial_class_regular():
    @dataclass
    class PartialClassRegular:
        field1: Optional[int] = None
        field2: Optional[str] = None
        field3: Optional[float] = None
        field4: Optional[bool] = None
        field5: Optional[str] = None

    return PartialClassRegular


def create_required_class_regular():
    @dataclass
    class RequiredClassRegular:
        field1: int
        field2: str
        field3: float
        field4: bool
        field5: str

    return RequiredClassRegular


def create_omitted_class_utility():
    return omit("OmittedClass", BaseClass, ["field2", "field4"])


def create_picked_class_utility():
    return pick("PickedClass", BaseClass, ["field2", "field4"])


def create_partial_class_utility():
    return partial("PartialClass", BaseClass)


def create_required_class_utility():
    return required("RequiredClass", BaseClass)


def benchmark(func, iterations):
    start_time = perf_counter()
    for _ in range(iterations):
        func()
    end_time = perf_counter()
    return end_time - start_time


def main():
    iterations = 10_000
    runs = 5

    benchmarks = {
        "Omit": (create_omitted_class_regular, create_omitted_class_utility),
        "Pick": (create_picked_class_regular, create_picked_class_utility),
        "Partial": (create_partial_class_regular, create_partial_class_utility),
        "Required": (
            create_required_class_regular,
            create_required_class_utility,
        ),
    }

    results = {name: {"Regular": [], "Utility": []} for name in benchmarks}

    for _ in range(runs):
        for name, (regular_func, utility_func) in benchmarks.items():
            results[name]["Regular"].append(benchmark(regular_func, iterations))
            results[name]["Utility"].append(benchmark(utility_func, iterations))

    table = []
    for name, times in results.items():
        avg_regular = sum(times["Regular"]) / runs
        avg_utility = sum(times["Utility"]) / runs
        ratio = avg_utility / avg_regular
        table.append(
            [
                name,
                f"{avg_regular:.6f}",
                f"{avg_utility:.6f}",
                f"{ratio:.2f}",
            ]
        )

    print(f"Benchmark results (average of {runs} runs, {iterations:_} iterations each):")
    print(
        tabulate(
            table,
            headers=["Transformation", "Regular (s)", "Utility (s)", "Utility ÷ Regular"],
        )
    )


if __name__ == "__main__":
    main()
