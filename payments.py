from genericpath import isfile
import json
import os

file_path = 'appdata/cash_book.json'
payment_book = 'appdata/payment_book.json'
data_book = 'appdata/data_book.json'
order_book = 'appdata/order_book.json'
ledger_path = 'appdata/ledger_book.json'

class UserPayments:

    def __init__(self, user_id, order_no, order_amount):
        if os.path.isfile(payment_book):
            with open(payment_book) as file:
                data = json.load(file)
                self.pay_no = len(data) + 1
        else:
            self.pay_no = 1

        self.user_id = user_id
        self.order_no = order_no
        self.order_amount = order_amount

    def get_balance(self):
        with open(data_book) as file:
            data = json.load(file)
            for item in data:
                if item['user_id'] == self.user_id:
                    return item['balance']

    def make_payment(self):
        order_cost = self.order_amount
        previous_balance = self.get_balance()
        balance = previous_balance - order_cost
        

        if balance > -1:
            if os.path.isfile(ledger_path):
                with open(ledger_path) as file:
                    data = json.load(file)
                    data.append({
                            'user_id': self.user_id,
                            'available_cash' : balance,
                            'previous_balance': previous_balance,
                            'last_amount_paid' : order_cost,
                                })
                    with open(ledger_path, 'w') as file:
                        json.dump(data, file, indent=4, separators=(',', ':'))

                        print('Paid')
            else:
                data = [{
                    'user_id': self.user_id,
                    'available_cash': balance,
                    'previous_balance': previous_balance,
                    'last_amount_paid': order_cost
                }]
                with open(ledger_path, 'w') as file:
                    json.dump(data, file, indent=4, separators=(',', ':')) 
        else:
            print('Insufficient Balance')
            return False

        payment_info = [{
            'pay_no':
            self.pay_no,
            'user_id':
            self.user_id,
            'order_no':
            self.order_no,
            'last_amount_paid': order_cost
        }]

        if os.path.isfile(payment_book):
            with open(payment_book) as file:
                payment_data = json.load(file)
                payment_data.append({
                    'pay_no':
                    self.pay_no,
                    'user_id':
                    self.user_id,
                    'order_no':
                    self.order_no,
                    'last_amount_paid': order_cost
                })

                with open(payment_book, 'w') as file:
                    json.dump(payment_data,
                                file,
                                indent=4,
                                separators=(',', ':'))
        else:
            with open(payment_book, 'w') as file:
                json.dump(payment_info,
                        file,
                        indent=4,
                        separators=(',', ':'))


        with open(data_book) as file:
            update_user_balance = json.load(file)

            for x in range(len(update_user_balance)):
                if update_user_balance[x]['user_id'] == self.user_id:
                    update_user_balance[x]['balance'] = balance
                    update_user_balance[x]['paid_transactions'].append(self.order_no)

                    with open(payment_book) as file:
                        data = json.load(file)
                        update_user_balance[x]['total_paid_amount'] = sum([data[x]['last_amount_paid'] for x in range(len(data)) if data[x]['user_id'] == self.user_id])


            with open(data_book, 'w') as file:
                json.dump(update_user_balance,
                            file,
                            indent=4,
                            separators=(',', ':'))
                print('Successful')

