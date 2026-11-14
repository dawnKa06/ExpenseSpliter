"""Simple Expense Splitter - a beginner-friendly terminal app."""

import csv

EXPORT_FILE = "expense_history.csv"


def get_total_expense():
    """Ask for the total expense until the user enters a valid, non-negative number."""
    while True:
        text = input("Enter the total expense amount: ").strip()
        try:
            amount = float(text)
        except ValueError:
            print("Oops! Please enter a number, for example 120 or 85.50.")
            continue

        # float("nan") and float("inf") are accepted by float(), so reject them.
        if amount != amount or amount in (float("inf"), float("-inf")):
            print("Oops! Please enter a normal number, for example 120 or 85.50.")
            continue

        if amount < 0:
            print("The expense cannot be negative. Please try again.")
            continue

        return amount


def get_number_of_people():
    """Ask for the number of people until the user enters a positive whole number."""
    while True:
        text = input("Enter the number of people: ").strip()
        try:
            people = int(text)
        except ValueError:
            print("Oops! Please enter a whole number, for example 3.")
            continue

        if people <= 0:
            print("The number of people must be at least 1. Please try again.")
            continue

        return people


def get_tip_percentage():
    """Ask for the tip percentage until the user enters a valid, non-negative number (0 is OK)."""
    while True:
        text = input("Enter the tip percentage (0 for no tip): ").strip()
        # Allow the user to type a trailing % sign, e.g. 15%
        if text.endswith("%"):
            text = text[:-1].strip()

        try:
            tip_percent = float(text)
        except ValueError:
            print("Oops! Please enter a number for the tip, for example 10 or 12.5.")
            continue

        # float("nan") and float("inf") are accepted by float(), so reject them.
        if tip_percent != tip_percent or tip_percent in (float("inf"), float("-inf")):
            print("Oops! Please enter a normal number for the tip, for example 10 or 12.5.")
            continue

        if tip_percent < 0:
            print("The tip cannot be negative. Please try again.")
            continue

        return tip_percent


def ask_yes_no(question):
    """Ask a yes/no question until the user answers. Returns True or False."""
    while True:
        answer = input(question).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please type 'y' for yes or 'n' for no.")


def show_history(history):
    """Print every calculation saved in the history list."""
    print("\n--- Calculation History ---")
    for number, entry in enumerate(history, start=1):
        print(
            f"{number}. Expense: {entry['expense']:.2f} | "
            f"Tip: {entry['tip_percent']:.2f}% | "
            f"People: {entry['people']} | "
            f"Each pays: {entry['share']:.2f}"
        )
    print("---------------------------")


def export_history_to_csv(history):
    """Save the calculation history to expense_history.csv (in the current folder)."""
    if not history:
        print("There is no calculation history to export yet.")
        return

    try:
        with open(EXPORT_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "Expense Amount",
                    "Tip Percentage",
                    "Number of People",
                    "Final Amount Per Person",
                ]
            )
            for entry in history:
                writer.writerow(
                    [
                        f"{entry['expense']:.2f}",
                        f"{entry['tip_percent']:.2f}",
                        entry["people"],
                        f"{entry['share']:.2f}",
                    ]
                )
    except OSError:
        print(
            f"Sorry, the history could not be saved to {EXPORT_FILE}. "
            "If the file is open in another program, please close it and try again."
        )
        return

    print(f"Success! Exported {len(history)} calculation(s) to {EXPORT_FILE}.")


def ask_to_repeat():
    """Ask if the user wants to do another calculation. Returns True or False."""
    while True:
        answer = input("\nDo you want to calculate again? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please type 'y' for yes or 'n' for no.")


def main():
    print("=== Expense Splitter ===")

    # History lives in memory only and is lost when the program closes.
    history = []

    while True:
        total = get_total_expense()
        people = get_number_of_people()

        tip_percent = get_tip_percentage()

        tip_amount = total * tip_percent / 100
        final_total = total + tip_amount
        share = final_total / people

        print(f"\nExpense:            {total:.2f}")
        print(f"Tip ({tip_percent:.2f}%):      {tip_amount:.2f}")
        print(f"Final total:        {final_total:.2f}")
        print(f"Each person should pay: {share:.2f}")

        # Save this successful calculation.
        history.append(
            {
                "expense": total,
                "tip_percent": tip_percent,
                "people": people,
                "share": share,
            }
        )

        if ask_yes_no("\nDo you want to view previous calculations? (y/n): "):
            show_history(history)

        if ask_yes_no("\nDo you want to export the history to CSV? (y/n): "):
            export_history_to_csv(history)

        if not ask_to_repeat():
            print("Thank you for using Expense Splitter. Goodbye!")
            break
        print()


if __name__ == "__main__":
    main()
