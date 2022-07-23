import json
import os

file_path = 'appdata/cash_book.json'
payment_book = 'appdata/completed_payment.json'
data_book = 'appdata/data_book.json'
order_book = 'appdata/order_book.json'
ledger_path = 'appdata/ledger_book.json'


class User:
    def __init__(self, username, first_name, last_name, full_name):

        if os.path.isfile(data_book):
            with open(data_book) as file:
                data = json.load(file)
                self.user_id = len(data) + 1
        else:
            self.user_id = 1

        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name
        self.pending_transactions = []
        self. paid_transactions = []
        self.total_paid_amount = 0
        # self.cash_book()
     

    def save_user(self):
        user_info = {}
        #TODO Automate user_id increment
        user_info['user_id'] = self.user_id
        user_info['username'] = self.username
        user_info['first_name'] = self.first_name
        user_info['last_name'] = self.last_name
        user_info['full_name'] = self.full_name
        user_info['pending_transactions'] = self.pending_transactions
        user_info['paid_transactions'] = self.paid_transactions
        user_info['total_paid_amount'] = self.total_paid_amount
        user_info['balance'] = 100000

        if os.path.isfile(data_book):
            with open(data_book) as file:
                data = json.load(file)
                data.append(user_info)

                with open(data_book, 'w') as file:
                    json.dump(data, file, indent=4, separators=(',',':'))
        else:
            with open(data_book, 'w') as file:
                json.dump([user_info], file, indent=4, separators=(',',':'))

        print('Details Saved')

    def cash_book(self):
        user_info = {}

        user_info['user_id'] = self.user_id
        user_info['available_cash'] = 100000
        user_info['previous_balance'] = 100000
        user_info['last_amount_paid'] = 0


        if os.path.isfile(ledger_path):
            with open(ledger_path) as file:
                data = json.load(file)
                data.append(user_info)

                with open(ledger_path, 'w') as file:
                    json.dump(data, file, indent=4, separators=(',',':'))
        else:
            with open(ledger_path, 'w') as file:
                json.dump([user_info], file, indent=4, separators=(',',':'))




