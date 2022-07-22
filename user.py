import json
import os
from transaction import Transactions


class User:
    def __init__(self, id, username, first_name, last_name, full_name):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name
        self.pending_transactions = []
        self. paid_transactions = []
        self.total_paid_amount = 0
        self.cash_book()


    # def credit_card_info(self):
    #     card_info = {}

    #     card_info['card_no'] =  input('Please type your card no: ')
    #     card_info['card_holder_name'] = input('Your fullname: ')
    #     card_info['expiration_date'] =  input('Expiration details: ')
    #     card_info['cvc_code'] = input('Card CVC code: ')

    #     return card_info
        

    def save_user(self):
        file_path = 'appdata/data.json'
        user_info = {}

        user_info['id'] = self.id
        user_info['username'] = self.username
        user_info['first_name'] = self.first_name
        user_info['last_name'] = self.last_name
        user_info['full_name'] = self.full_name
        user_info['pending_transactions'] = self.pending_transactions
        user_info['paid_transactions'] = self.paid_transactions
        user_info['total_paid_amount'] = self.total_paid_amount
        user_info['balance'] = 100000
        # user_info['card_details'] = self.credit_card_info()

        if os.path.isfile(file_path):
            with open(file_path) as file:
                data = json.load(file)
                data.append(user_info)

                with open(file_path, 'w') as file:
                    json.dump(data, file)
        else:
            with open(file_path, 'w') as file:
                json.dump([user_info], file, indent=4, separators=(',',':'))

        print('Details Saved')

    def cash_book(self):
        file_path = 'appdata/cash_book.json'
        user_info = {}

        user_info['id'] = self.id
        user_info['username'] = self.username
        user_info['available_cash'] = 10000
        user_info['previous_balance'] = 10000
        user_info['last_amount_paid'] = 0


        if os.path.isfile(file_path):
            with open(file_path) as file:
                data = json.load(file)
                data.append(user_info)

                with open(file_path, 'w') as file:
                    json.dump([data], file, indent=4, separators=(',',':'))
        else:
            with open(file_path, 'w') as file:
                json.dump([user_info], file, indent=4, separators=(',',':'))




