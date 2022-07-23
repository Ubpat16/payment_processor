import json
import os
import random
from payment_processors import Credit, PayPal, Bank
import time

file_path = 'appdata/cash_book.json'
payment_book = 'appdata/completed_payment.json'
data_book = 'appdata/data_book.json'
order_book = 'appdata/order_book.json'


class UserTransactions:

    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.confirmation_code = random.randint(1000, 9999)
        self.status = ''
        self.amount = 0

    def place_order(self):
        user_id = self.user_id
        if os.path.isfile(order_book):
            with open(order_book) as file:
                data = json.load(file)
                order_no = len(data) + 1
        else:
            order_no = 1

        #TODO populate a product and assign prices to them
        products = {
            'school_fees': 30000,
            'mobile_plan': 500,
            'groceries': 300,
            'food': 5
        }

        feedback = input('Start your order, "y" for Yes, any other key to exit: ').lower()
        if feedback == 'y':
            print(
                'Available Products are "School fees = 30000, Mobile Plans = 500, Groceries = 300, Food = 50: "'
            )
            order = input(
                '"s" for School fees, "m" for Mobile Plans, "g" for Groceries, "f" for Food: '
            ).lower()

            if order == 's':
                order_amount = products['school_fees']
            elif order == 'm':
                order_amount = products['mobile_plan']
            elif order == 'g':
                order_amount = products['groceries']
            elif order == 'f':
                order_amount = products['food']
        else:
            return



        prompt = int(
            input(
                'Do you want to complete your order now? Please type (1) to PAY NOW, (2) to PAY LATER, (3) to Cancel: '
            ))


        if prompt == 1:
            self.status = 'Paid'
            print("Now proceeding to Payment")
            choose_payment_gateway = input('Please choose your method of payment? "C" for Credit Card Purchases, "P" for PayPal and "B" for Bank Transfers: ').lower()
            prompt = int(input(f'\nHi, Your confirmation code is {self.confirmation_code}, type the code here to proceed: '))
            if choose_payment_gateway == 'c':
                if prompt == self.confirmation_code:
                    print(f'{self.username} Authorized\n')
                    time.sleep(1)
                    Credit(user_id=self.user_id, order_no=order_no, order_amount=order_amount)
                else:
                    print('Wrong Code! Unauthorized User!\n')
                    return
            elif choose_payment_gateway == 'p':
                if prompt == self.confirmation_code:
                    print(f'{self.username} Authorized\n')
                    PayPal(user_id=self.user_id, username=self.username, order_no=order_no, order_amount=order_amount)
                else:
                    print('Wrong Code! Unauthorized User!\n')
                    return

            elif choose_payment_gateway == 'b':
                if prompt == self.confirmation_code:
                    print(f'{self.username} Authorized\n')
                    Bank(user_id=self.user_id, order_no=order_no, order_amount=order_amount)
                else:
                    print('Wrong Code! Unauthorized User!\n')
                    return

        elif prompt == 2:
            self.status == 'Pending'
            print('Order is pending, I will remind you later')
            with open(data_book) as file:
                data = json.load(file)
                for x in range(len(data)):
                    if data[x]['user_id'] == user_id:
                        data[x]['pending_transactions'].append(order_no)
                with open(data_book, 'w') as file:
                    json.dump(data, file, indent=4, separators=(',', ':'))

        elif prompt == 3:
            self.status == 'Cancel'
            print('Oops! Wrong choice, I hope to see you again')
            return


        orders = {
            "user_id": user_id,
            "order_no": order_no,
            "order_amount": order_amount
        }
        if os.path.isfile(order_book) is False:
            with open(order_book, 'w') as file:
                json.dump([orders], file, indent=4, separators=(',', ':'))
        else:
            with open(order_book) as file:
                data = json.load(file)
                data.append(orders)

                with open(order_book, 'w') as file:
                    json.dump(data, file, indent=4, separators=(',', ':'))