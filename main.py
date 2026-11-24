"""Interactive entry point for the string-matching engine."""

from benchmark import ALGORITHMS, benchmark, print_results
from demo import choose_demo
from utils import prompt_for_input, read_input_file


def settings(use_file):
    while True:
        print("\nSettings")
        print(f"Current input source: {'input.txt' if use_file else 'runtime prompts'}")
        print("1. Enter text and pattern at runtime")
        print("2. Read from input.txt")
        print("3. Back to main menu")
        choice = input("Select an option: ").strip()
        if choice == "1":
            return False
        if choice == "2":
            return True
        if choice == "3":
            return use_file
        print("Choose 1, 2, or 3.")


def engine(use_file):
    while True:
        print("\nString Matching Engine")
        for option, algorithm in ALGORITHMS.items():
            print(f"{option}. {algorithm[0]}")
        print("5. Run and benchmark all")
        print("6. Benchmark a random demo")
        print("7. Back to main menu")

        choice = input("Select an option: ").strip()
        if choice == "7":
            return
        if choice not in ALGORITHMS and choice not in ("5", "6"):
            print("Choose an option from 1 to 7.")
            continue

        if choice == "6":
            text, pattern = choose_demo()
            print(f"\nDemo text: {text!r}")
            print(f"Demo pattern: {pattern!r}")
        elif use_file:
            try:
                text, pattern = read_input_file()
            except ValueError as error:
                print(f"\nInput file is missing or configured incorrectly. {error}")
                return
        else:
            text, pattern = prompt_for_input()

        algorithms = (ALGORITHMS[choice],) if choice in ALGORITHMS else ALGORITHMS.values()
        results = [benchmark(algorithm, text, pattern) for algorithm in algorithms]
        print_results(results, len(text), len(pattern))


def main():
    use_file = False
    while True:
        print("\nMain Menu")
        print("1. Enter the engine")
        print("2. Settings")
        print("3. Exit")
        choice = input("Select an option: ").strip()
        if choice == "1":
            engine(use_file)
        elif choice == "2":
            use_file = settings(use_file)
        elif choice == "3":
            return
        else:
            print("Choose 1, 2, or 3.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print()
