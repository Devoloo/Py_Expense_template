from PyInquirer import prompt
import csv
import ast

def get_users():
    users_list = []
    with open("./users.csv", 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            users_list.append(row[1])

    return users_list

def get_users_ids():
    users_list = []
    with open("./users.csv", 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            users_list.append(row)
    
    return users_list

def list_to_dict(list):
    list_dict = []
    for n in list:
        dict = {}
        dict['name'] = n
        list_dict.append(dict)
    
    return list_dict

expense_questions = [
    {
        "type":"input",
        "name":"amount",
        "message":"New Expense - Amount: ",
    },
    {
        "type":"input",
        "name":"label",
        "message":"New Expense - Label: ",
    },
    {
        "type":"list",
        "name":"spender",
        "message":"New Expense - Spender:",
        "choices": get_users()
    },
    {
        "type":"checkbox",
        "name":"users",
        "message":"Select users - Users:",
        "choices": list_to_dict(get_users())
    }
]

def write_expense(infos, exp_id):
    f = open("expense_report.csv","a")
    
    infos['id'] = exp_id
    
    users_list = get_users_ids()
    spender_id = 0
    # find user id of infos['spender']
    for user in users_list:
        if user[1] == infos['spender']:
            spender_id = user[0]
            break
    # user id found instead of name
    infos['spender'] = spender_id

    # do the same thing for users
    users_list = get_users_ids()
    users_id = []
    for user in users_list:
        for u in infos['users']:
            if user[1] == u:
                users_id.append(user[0])
                break

    infos['users'] = users_id

    f.write(f'{infos["id"]},{infos["label"]},{infos["amount"]},{infos["spender"]}\n')
    
    return spender_id, users_id

def add_expense_to_spender(infos, spender_id, users_id):
    with open("users.csv", "r") as f:
        csv_reader = csv.reader(f)
        data = list(csv_reader)

    # data[int(spender_id)][2] = float(infos['amount']) - ((float(data[int(spender_id)][2]) + float(infos['amount'])) / (len(users_id)))

    with open("users.csv", "w") as f:
        for line in data:
            f.write(f'{line[0]},{line[1]},{line[2]}\n')
    
    # remove the amout to the other users
    remove_amount_to_other_users(infos, spender_id, infos['users'])

    return True

def remove_amount_to_other_users(infos, spender_id, users_list):
    with open("users.csv", "r") as f:
        csv_reader = csv.reader(f)
        data = list(csv_reader)

    print(data)
    amount = float(infos['amount']) / len(users_list)

    for row in data:
        if row[0] in users_list and row[0] != spender_id:
            
            last_element_str = row[-1]  # Get the last element as a string
            try:
                # Safely evaluate the string representation to get a Python list
                last_element_list = ast.literal_eval(last_element_str)
                row[-1] = last_element_list  # Replace the string with the Python list
            except (ValueError, SyntaxError):
                # Handle the case where the string cannot be evaluated as a list
                print(f"Unable to convert '{last_element_str}' to a list")

    # Now, 'data' contains the lists as the last elements in each row, and you can work with them
    for row in data:
        if row[0] in users_list and row[0] != spender_id:
            print(row)
            row[2].append([amount, spender_id])

    with open("users.csv", "w") as f:
        for line in data:
            f.write(f'{line[0]},{line[1]},{line[2]}\n')
    
    return True

def new_expense(exp_id):
    infos = prompt(expense_questions)
    spender_id, users_id = write_expense(infos, exp_id)
    add_expense_to_spender(infos, spender_id, users_id)
    exp_id += 1
    print("Expense Added !")
    return exp_id