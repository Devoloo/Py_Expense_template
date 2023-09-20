from PyInquirer import prompt
import csv

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

    data[int(spender_id)][2] = float(infos['amount']) - ((float(data[int(spender_id)][2]) + float(infos['amount'])) / (len(users_id)))

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

    amount = float(infos['amount']) / len(users_list)

    for i in users_list:
        if i != spender_id:
            print(i, spender_id)
            data[int(i)][2] = float(data[int(i)][2]) - amount

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