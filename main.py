from PyInquirer import prompt
from expense import new_expense
from user import add_user

def count_ids(f_name):
    f = open(f_name,"r")
    count = len(f.readlines())

    return count


def ask_option():
    main_option = {
        "type":"list",
        "name":"main_options",
        "message":"Expense Tracker v0.1",
        "choices": ["New Expense","Show Status","New User"]
    }

    option = prompt(main_option)

    # Get the current number of ID in the expense report
    count_exp = count_ids("expense_report.csv")
    count_user = count_ids("users.csv")

    if (option['main_options']) == "New Expense":
        count_exp = new_expense(count_exp)
        ask_option()

    if (option['main_options']) == "Show Status":
        print("Show Status")
        ask_option()

    if (option['main_options']) == "New User":
        count_user = add_user(count_user)
        ask_option()

def main():
    ask_option()

main()