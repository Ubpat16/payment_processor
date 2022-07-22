import json
import os
import random

file_path = 'appdata/cash_book.json'
payment_book = 'appdata/completed_payment.json'
data_book = 'appdata/data.json'
order_book = 'appdata/order_book.json'


class Transactions:
    def __init__(self, id, user):
        self.id = id
        self.confirmation_code = random.randint(1000, 9999)
        self.user = user
        self.status = ''
        self.amount = 0

    def get_balance(self, id):
        with open(data_book) as file:
            data = json.load(file)
            for item in data:
                if item['id'] == id:
                    return item['balance']

    def place_order(self, id, user):
        id = self.id
        user = self.user

        pay_now = False
        pay_later = False
        cancel = False
        order = False


        feedback = input('Start your order: ').lower()
        if feedback == 'y':
            order = True
            while order:
                amount = int(input('Place your order amount: '))
                self.amount = amount
                order_no = random.randint(1, 100)
                prompt = int(input('Do you want to complete your order now? Please type (1) to PAY NOW, (2) to PAY LATER, (3) to Cancel: '))
                
                with open('appdata/data.json') as file:
                    update_user = json.load(file)
                
                for x in range(len(update_user)):
                    if update_user[x]['username'] == self.user:
                        if prompt == 1:
                            self.status = 'Paid'
                            update_user[x]['paid_transactions'].append(order_no)
                            print("Now proceeding to Payment")
                            self.make_payment(id=id, user=user)
                        
                        elif prompt == 2:
                            self.status == 'Pending'
                            update_user[x]['pending_transactions'].append(order_no)

                        elif prompt == 3:
                            self.status == 'Cancel'

                with open('appdata/data.json', 'w') as file:
                    json.dump(update_user,
                            file,
                            indent=4,
                            separators=(',', ':'))
                
                feedback = input("It\'s still a good day to shop? Place a new order? (Y) for Yes, (N) for No: ").lower()
                if feedback == 'y':
                    order = True
                else:
                    order = False




    def make_payment(self, id, user):
        order_cost = self.amount
        previous_balance = self.get_balance(id=id)
        payment = previous_balance - order_cost
        temp_data = {}

        if payment > -1:
            with open(file_path) as file:
                data = json.load(file)
                for x in range(len(data)):
                    if data[x]['id'] == id:
                        temp_data['index'] = x
                        temp_data['id'] = id
                        temp_data['username'] = user
                        temp_data['available_cash'] = payment
                        temp_data['previous_balance'] = previous_balance
                        temp_data['last_amount_paid'] = order_cost

            data[temp_data['index']] = {
                'id': temp_data['id'],
                'username': temp_data['username'],
                'previous_balance': temp_data['previous_balance'],
                'available_cash': temp_data['available_cash'],
                'last_amount_paid': temp_data['last_amount_paid']
            }
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4, separators=(',', ':'))

                print('Paid')
        else:
            print('Insufficient Balance')

        if len(temp_data) > 0:
            if os.path.isfile(payment_book):
                with open(payment_book) as file:
                    orders = json.load(file)
                    orders.append({
                        'id':
                        temp_data['id'],
                        'username':
                        temp_data['username'],
                        'last_amount_paid':
                        temp_data['last_amount_paid']
                    })

                    with open(payment_book, 'w') as file:
                        json.dump(orders,
                                  file,
                                  indent=4,
                                  separators=(',', ':'))
            else:
                with open(payment_book, 'w') as file:
                    json.dump(
                        [{
                            'id': temp_data['id'],
                            'username': temp_data['username'],
                            'last_amount_paid': temp_data['last_amount_paid']
                        }],
                        file,
                        indent=4,
                        separators=(',', ':'))

            with open('appdata/data.json') as file:
                update_user = json.load(file)
                for x in range(len(update_user)):
                    if update_user[x]['username'] == self.user:
                        update_user[x]['balance'] = temp_data['available_cash']

                with open('appdata/data.json', 'w') as file:
                    json.dump(update_user,
                              file,
                              indent=4,
                              separators=(',', ':'))
