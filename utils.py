"""Input helpers for the engine."""

from pathlib import Path


ENGINE_DIRECTORY = Path(__file__).resolve().parent
INPUT_FILENAME = "input.txt"


def read_input_file():
    try:
        path = next((entry for entry in ENGINE_DIRECTORY.iterdir() if entry.name == INPUT_FILENAME),None)
        if path is None:
            raise FileNotFoundError(INPUT_FILENAME)
        with path.open(encoding="utf-8-sig") as input_file:
            lines = [line.rstrip("\n") for line in input_file]
    except (OSError, UnicodeError) as error:
        raise ValueError("Place a readable input.txt text file in the engine directory.") from error

    values = {}
    for line in lines:
        key, separator, value = line.partition("=")
        if separator != "=" or key not in ("T", "P") or key in values:
            raise ValueError("Use exactly one T= line and one P= line.")
        values[key] = value

    if len(values) != 2:
        raise ValueError("Use exactly one T= line and one P= line.")
    return values["T"], values["P"]


def prompt_for_input():
    text = input("Text (T): ")
    pattern = input("Pattern (P): ")
    return text, pattern
