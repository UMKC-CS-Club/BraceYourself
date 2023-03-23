import json

from KnotContainer import KnotContainer


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


def prompt_load_file(prompt, loader):
    print(prompt)

    while True:
        f_name = input("> ")
        try:
            f = open(f_name)
        except FileNotFoundError:
            print(f"Couldn't find a file at {f_name}. Please try another path.")
            continue

        with f:
            loaded, ret = loader(f)
            if loaded:
                return ret

            print(f"Couldn't load from the file at {f_name}. Please try another file.")


def prompt_user_canvas():
    n_strings = 12
    n_primary_rows = 12
    return KnotContainer.empty(n_strings, n_primary_rows)


def prompt_user_save():
    def loader(file):
        try:
            return True, KnotContainer.from_dict(json.load(file))
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            return False, None

    return prompt_load_file("Enter the path of the file to load:", loader)


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


