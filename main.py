import json
import os
from user import User
from transaction import UserTransactions

app_data = 'appdata'
if os.path.isdir(app_data):
    pass
else:
    os.mkdir('appdata')

data_book = 'appdata/data_book.json'
print("Hi, Welcome!")

prompt = input('Do you have an Accout? "n" to create a new one. "y" to login an existing one: ').lower()

if prompt == 'y':
    username = input('Your registered Username: ').lower()
    with open(data_book) as file:
        user_login = json.load(file)
        users = []
        for item in user_login:
            users.append(item['username'])
        
        if username in users:
            user_id = item['user_id']

            user_transaction = UserTransactions(user_id=user_id, username=username)
            user_transaction.place_order()
        else:
            print('\nUsername not found, Please register again if you forgot the name you used or check "appdata/data_book.json"\n')


elif prompt == 'n':

    if os.path.isfile(data_book) == False:
        username = input('Your preferred Username: ').lower()
        firstname = input('Your preferred firstname: ').lower()
        lastname = input('Your preferred lastname: ').lower()
        fullname = f'{firstname} {lastname}'

        user = User(username=username, first_name=firstname, last_name=lastname, full_name=fullname)
        user.save_user()

        with open(data_book) as file:
            user_detail = json.load(file)
            for item in user_detail:
                if item['username'] == username:
                    user_id = item['user_id']

        user_transaction = UserTransactions(user_id=user_id, username=username)
        user_transaction.place_order()

    else:       
        username = input('Your preferred Username: ').lower()
        with open(data_book) as file:
            records = json.load(file)
            for x in range(len(records)):
                if records[x]['username'] == username:
                    print(f'{username} is taken already!')
                else:
                    firstname = input('Your preferred firstname: ').lower()
                    lastname = input('Your preferred lastname: ').lower()
                    fullname = f'{firstname} {lastname}'

                    user = User(username=username, first_name=firstname, last_name=lastname, full_name=fullname)
                    user.save_user()

                    with open(data_book) as file:
                        user_detail = json.load(file)
                        for item in user_detail:
                            if item['username'] == username:
                                user_id = item['user_id']

                    user_transaction = UserTransactions(user_id=user_id, username=username)
                    user_transaction.place_order()