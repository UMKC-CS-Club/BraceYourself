import json
from dataclasses import dataclass
from typing import Any, Callable, Union, Optional

from KnotContainer import KnotContainer


@dataclass
class Success:
    value: Any


@dataclass
class Failure:
    message: str


Result = Union[Success, Failure]
Numeric = Union[int, float]


def prompt_user(prompt: str, validator_extractor: Callable[[str], Result]):
    while True:
        inp = input(prompt)
        result = validator_extractor(inp)
        if isinstance(result, Success):
            return result.value

        print(result.message)


def make_inclusive_range_validator(lower: Numeric, upper: Numeric) -> Callable[[Numeric], bool]:
    def range_validator(num):
        return lower <= num <= upper

    return range_validator


def prompt_number(prompt, lower, upper):
    validator = make_inclusive_range_validator(lower, upper)

    def validator_extractor(inp):
        num = int(inp)
        if validator(num):
            return Success(num)

        return Failure(f"Number is not in range [{lower}, {upper}]")

    return prompt_user(prompt, validator_extractor)


def prompt_options(prompt, options):
    print(prompt)
    for i, option in enumerate(options):
        print(f"{i + 1} - {option}")

    while True:
        choice = input(f"(1 - {len(options)}) > ")
        try:
            return options[int(choice) - 1]
        except ValueError:
            print(f"{choice} doesn't appear to be a number. Please try again.")
        except IndexError:
            print(f"{choice} doesn't appear to be between 1 and {len(options)}. Please try again.")


def prompt_load_file(prompt, extractor_validator):
    def _extractor_validator(f_name):
        try:
            f = open(f_name)
        except FileNotFoundError:
            return Failure(f"Couldn't find a file at {f_name}. Please try another path.")

        with f:
            return extractor_validator(f)

    return prompt_user(prompt, _extractor_validator)


def prompt_user_canvas():
    n_strings = prompt_number("How many strings? ", 2, float("inf"))
    n_primary_rows = prompt_number("How many pairs of rows? ", 1, float("inf"))
    return KnotContainer.empty(n_strings, n_primary_rows)


def prompt_user_save():
    def loader(f_name):
        try:
            return Success(KnotContainer.from_dict(json.load(f_name)))
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            return Failure(f"Couldn't load from the file at {f_name}. Please try another file.")

    return prompt_load_file("Enter the path of the file to load: ", loader)


def get_knot_container():
    options = {"Load from a file": prompt_user_save, "Create a new canvas": prompt_user_canvas}
    selection = prompt_options("Would you like to:", list(options.keys()))
    return options[selection]()


def prompt_save(knots):
    selection = prompt_options("Would you like to:", ["Save", "Quit without saving"])

    if selection.startswith("Quit"):
        return

    f_name = input("Enter the path of the file to write to: ")

    with open(f_name, 'w') as f:
        json.dump(knots.to_dict(), f)


