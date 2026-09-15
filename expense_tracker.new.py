import csv
import os
import matplotlib.pyplot as plt


FILE_NAME = "expenses.csv"
expenses = []


def load_expenses():
    """Load expenses from the CSV file."""

    if not os.path.exists(FILE_NAME):
        return

    try:
        with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    expense = {
                        "date": row["date"],
                        "category": row["category"],
                        "amount": float(row["amount"])
                    }

                    expenses.append(expense)

                except (ValueError, KeyError):
                    print("Skipped an invalid record in the CSV file.")

    except Exception as e:
        print("Error loading expenses:", e)


def save_expenses():
    """Save expenses to the CSV file."""

    try:
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:

            fieldnames = ["date", "category", "amount"]

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(expenses)

        print("\nExpenses saved successfully!")

    except Exception as e:
        print("Error saving expenses:", e)


def add_expense():
    """Add a new expense."""

    print("\n===== Add Expense =====")

    date = input("Enter date (YYYY-MM-DD): ").strip()
    category = input("Enter category: ").strip()

    while True:
        amount_text = input("Enter amount: ").strip()

        try:
            amount = float(amount_text)

            if amount < 0:
                print("Amount cannot be negative.")
                continue

            break

        except ValueError:
            print("Invalid amount. Please enter a number.")

    expense = {
        "date": date,
        "category": category,
        "amount": amount
    }

    expenses.append(expense)

    print("\nExpense added successfully!")


def view_expenses():
    """Display all expenses."""

    print("\n===== All Expenses =====")

    if len(expenses) == 0:
        print("No expenses recorded.")
        return

    for number, expense in enumerate(expenses, start=1):

        print(f"\nExpense {number}")
        print("Date:", expense["date"])
        print("Category:", expense["category"])
        print("Amount:", f"{expense['amount']:.2f}")
        print("------------------------")


def generate_report():
    """Generate an expense report."""

    print("\n===== Expense Report =====")

    if len(expenses) == 0:
        print("No expenses recorded.")
        return

    total = 0
    category_totals = {}

    for expense in expenses:

        amount = expense["amount"]
        category = expense["category"]

        total += amount

        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

    print(f"\nTotal Spending: {total:.2f}")

    print("\nSpending by Category:")

    for category, amount in category_totals.items():
        print(f"{category}: {amount:.2f}")

    highest = max(expenses, key=lambda x: x["amount"])

    print("\nHighest Expense:")
    print("Date:", highest["date"])
    print("Category:", highest["category"])
    print("Amount:", f"{highest['amount']:.2f}")


def delete_expense():
    """Delete an expense."""

    print("\n===== Delete Expense =====")

    if len(expenses) == 0:
        print("No expenses recorded.")
        return

    view_expenses()

    try:
        number = int(input("\nEnter the expense number to delete: "))

        if number < 1 or number > len(expenses):
            print("Invalid expense number.")
            return

        deleted = expenses.pop(number - 1)

        print("\nExpense deleted successfully!")
        print("Deleted category:", deleted["category"])
        print("Deleted amount:", f"{deleted['amount']:.2f}")

    except ValueError:
        print("Please enter a valid expense number.")


def edit_expense():
    """Edit an existing expense."""

    print("\n===== Edit Expense =====")

    if len(expenses) == 0:
        print("No expenses recorded.")
        return

    view_expenses()

    try:
        number = int(input("\nEnter the expense number to edit: "))

        if number < 1 or number > len(expenses):
            print("Invalid expense number.")
            return

        expense = expenses[number - 1]

        print("\nPress Enter to keep the current value.")

        new_date = input(
            f"Enter new date [{expense['date']}]: "
        ).strip()

        new_category = input(
            f"Enter new category [{expense['category']}]: "
        ).strip()

        new_amount = input(
            f"Enter new amount [{expense['amount']}]: "
        ).strip()

        if new_date != "":
            expense["date"] = new_date

        if new_category != "":
            expense["category"] = new_category

        if new_amount != "":
            try:
                amount = float(new_amount)

                if amount < 0:
                    print("Amount cannot be negative.")
                    return

                expense["amount"] = amount

            except ValueError:
                print("Invalid amount. Expense was not updated.")
                return

        print("\nExpense updated successfully!")

    except ValueError:
        print("Please enter a valid expense number.")


def show_chart():
    """Display a bar chart of spending by category."""

    if len(expenses) == 0:
        print("\nNo expenses available for the chart.")
        return

    category_totals = {}

    for expense in expenses:

        category = expense["category"]
        amount = expense["amount"]

        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    plt.figure(figsize=(8, 5))

    plt.bar(categories, amounts)

    plt.title("Spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")

    plt.tight_layout()
    plt.show()


def main():
    """Main menu."""

    load_expenses()

    while True:

        print("\n================================")
        print("     PERSONAL EXPENSE TRACKER")
        print("================================")

        print("1. Add an Expense")
        print("2. View All Expenses")
        print("3. Generate Report")
        print("4. Delete an Expense")
        print("5. Edit an Expense")
        print("6. Show Spending Chart")
        print("7. Save and Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            generate_report()

        elif choice == "4":
            delete_expense()

        elif choice == "5":
            edit_expense()

        elif choice == "6":
            show_chart()

        elif choice == "7":
            save_expenses()
            print("\nThank you for using Personal Expense Tracker!")
            break

        else:
            print(
                "Invalid choice. "
                "Please enter a number from 1 to 7."
            )


if __name__ == "__main__":
    main()
