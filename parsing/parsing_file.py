from typing import Any
from parsing.valid_file_input import ValidFileInput
from pydantic import ValidationError
import sys


# Read the file config.txt and return the content
def get_file_content(file_name: str) -> list[str]:
    with open(file_name, "r") as file:
        content = file.readlines()
    return [line.strip("\n") for line in content]


# Get the content in the input_file and tranform it into variable
def transform_input(
    file_name: str, file_content: list[str]
) -> dict[str, Any]:
    """
    Parse and validate a maze config file.

    The function reads the configuration lines,
    ignores comments, extracts the required settings
    and convert them into a dictionnary
    """
    settings = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
        "SEED",
        "DISPLAY_SOLUTION",
    ]

    return_value: dict[str, Any] = {}
    for data in file_content:
        if not data:
            raise ValueError(
                "File input is invalid : no empty lines are allowed"
            )
        if data[0] == "#":
            continue
        if "=" not in data:
            raise ValueError("File input is invalid : no '=' detected")

        key, value = data.split("=", 1)
        if not key or key not in settings:
            continue

        if key in ("ENTRY", "EXIT"):
            if "," not in value:
                raise ValueError(
                    "File input is invalid : no ',' detected"
                )
            x, y = value.split(",", 1)
            if not x or not y:
                raise ValueError(
                    "File input is invalid : the value can't be empty"
                )
            return_value[key] = (x, y)
        else:
            return_value[key] = value
        settings.remove(key)

    if settings:
        raise ValueError(
            f"Missing settings to create the maze: {', '.join(settings)}"
        )

    if file_name == return_value["OUTPUT_FILE"]:
        raise ValueError("Input and output files can't be the same")

    return return_value


# Check if the input is valid, check with valid_file_input
def parse_input_file(file_name: str) -> ValidFileInput:
    """
    Parse and validate a maze input config file.

    The function reads the file content, extracts the configuration
    settings, and creates a validation ValidFileInput
    """
    try:
        file_content = get_file_content(file_name)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(-1)

    try:
        settings = transform_input(file_name, file_content)
        maze_input = ValidFileInput(
            width=settings["WIDTH"],
            height=settings["HEIGHT"],
            entry_x=settings["ENTRY"][0],
            entry_y=settings["ENTRY"][1],
            exit_x=settings["EXIT"][0],
            exit_y=settings["EXIT"][1],
            output_filename=settings["OUTPUT_FILE"],
            is_perfect=settings["PERFECT"],
            seed=settings["SEED"],
            display_solution=settings["DISPLAY_SOLUTION"],
        )
    except ValidationError as e:
        print(e.errors()[0]["msg"], file=sys.stderr)
        sys.exit(-1)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(-1)

    return maze_input
