import csv
import matplotlib.pyplot as plt

# function to add expense
def add_expense():
    amount = input("Enter amount: ")
    category = input("Enter category: ")
    date = input("Enter date: ")
    note = input("Enter note: ")

    with open("expenses.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([amount, category, date, note])

    print("Expense Saved!\n")

# function to view expenses
def view_expenses():
    try:
        with open("expenses.csv", "r") as file:
            reader = csv.reader(file)
            
            total = 0
            category_sum = {}

            print("\nAll Expenses:")
            for row in reader:
                print(row)

                amount = float(row[0])
                category = row[1]

                total += amount

                if category in category_sum:
                    category_sum[category] += amount
                else:
                    category_sum[category] = amount

            print("\nTotal Expense:", total)

            print("\nCategory-wise Expense:")
            for cat, amt in category_sum.items():
                print(cat, ":", amt)

    except FileNotFoundError:
        print("No expenses found.\n")

def show_graph():
    try:
        with open("expenses.csv", "r") as file:
            reader = csv.reader(file)

            category_sum = {}

            for row in reader:
                amount = float(row[0])
                category = row[1]

                if category in category_sum:
                    category_sum[category] += amount
                else:
                    category_sum[category] = amount

            categories = list(category_sum.keys())
            amounts = list(category_sum.values())

            plt.bar(categories, amounts)
            plt.xlabel("Category")
            plt.ylabel("Amount")
            plt.title("Expenses by Category")
            plt.show()

    except FileNotFoundError:
        print("No expenses found.\n")

# main menu
while True:
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Show Graph")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        show_graph()
    elif choice == "4":
        break
    else:
        print("Invalid choice\n")