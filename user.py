from PyInquirer import prompt
user_questions = [
    {
        "type":"input",
        "name":"name",
        "message":"New User - Name: ",
    },
]

def write_user(infos, user_id):
    f = open("users.csv","a")
    infos['id'] = user_id
    infos['balance'] = 0
    f.write(f'{infos["id"]},{infos["name"]},{infos["balance"]}\n')
    return True

def add_user(user_id):
    infos = prompt(user_questions)
    write_user(infos, user_id)
    user_id += 1
    print("User Added !")
    return user_id