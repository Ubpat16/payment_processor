from genericpath import isfile
import json
import os


class User:
    def __init__(self, id, username, first_name, last_name, full_name, pending_transactions, paid_transactions, total_paid_amount):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name
        self.pending_transactions = pending_transactions
        self. paid_transactiosn = paid_transactions
        self.total_paid_amount = total_paid_amount


    def credit_card_info(self):
        card_info = {}

        card_info['card_no'] =  input('Please type your card no: ')
        card_info['card_holder_name'] = input('Your fullname: ')
        card_info['expiration_date'] =  input('Expiration details: ')
        card_info['cvc_code'] = input('Card CVC code: ')

        return card_info
        

    def save_user(self):
        file_path = 'appdata/data.json'
        user_info = {}

        user_info['user_id'] = self.id
        user_info['username'] = self.username
        user_info['first_name'] = self.first_name
        user_info['last_name'] = self.last_name
        user_info['full_name'] = self.full_name
        user_info['pending_transactions'] = self.pending_transactions
        user_info['paid_transaction'] = self.paid_transactiosn
        user_info['total_paid_amount'] = self.total_paid_amount
        user_info['card_details'] = self.credit_card_info()

        if os.path.isfile(file_path):
            updates = []
            with open(file_path) as file:
                data = json.load(file)
                data.append(user_info)

                with open(file_path, 'w') as file:
                    json.dump(data, file)
        else:
            with open(file_path, 'w') as file:
                json.dump([user_info], file, indent=4, separators=(',',':'))

        print('Details Saved')            



