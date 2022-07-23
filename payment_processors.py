from genericpath import isfile
import json
import os
import time
from payments import UserPayments
import datetime as dt
from user import User

file_path = 'appdata/cash_book.json'
payment_book = 'appdata/completed_payment.json'
data_book = 'appdata/data_book.json'
order_book = 'appdata/order_book.json'
paypal_records = 'appdata/paypal_logins.json'


class Credit:

    def __init__(self, user_id, order_no, order_amount):
        #TODO Check if user has card saved already.
        self.user_id = user_id
        self.order_no = order_no
        self.order_amount = order_amount

        with open(data_book) as file:
            user_data = json.load(file)
            for x in range(len(user_data)):
                if user_data[x]['user_id'] == self.user_id and 'card_information' in user_data[x].keys():
                    self.proceed()
                else:
                    self.credit_card_info(user_id)
    def proceed(self):
        prompt = input('Is this a one time Payment or Subscription: "t" for One Time Payment, "s" for subscription or a Refund Request "r"?: ').lower()
        if prompt == 't':
            self.one_time_payments()
        elif prompt == 's':
            self.subscription_payments()
        elif prompt == 'r':
            self.refunds()

    def credit_card_info(self, user_id):
        card_info = {}

        card_info['card_no'] =  input('Please type your card no: ')
        card_info['card_holder_name'] = input('Your fullname: ')
        card_info['expiration_date'] =  input('Expiration details: ')
        card_info['cvc_code'] = input('Card CVC code: ')

        prompt = input('Do you want to save your card information? ').lower()
        if prompt == 'y':
            with open(data_book) as file:
                data = json.load(file)
                for x in range(len(data)):
                    if data[x]['user_id'] == user_id:
                        data[x]['card_information'] = card_info

                with open(data_book, 'w') as file:
                    json.dump(data, file, indent=4, separators=(',',':'))
                    print('Your card information has been saved')
        self.proceed()

    
    def one_time_payments(self):
        user_payment = UserPayments(self.user_id, self.order_no, self.order_amount)
        pay = user_payment.make_payment()
        if pay == False:
            return
        else:
            self.print_invoice()

    def subscription_payments(self):
        user_payment = UserPayments(self.user_id, self.order_no, self.order_amount)
        print('Subscription payments are timedbased, so you will be charged every 30Days (3s) for the next 90Days')
        time.sleep(1)
        prompt = input('Type "y" to proceed ').lower()
        if prompt == 'y':
            total_order = user_payment.order_amount
            monthly_payment = total_order/3
            for x in range(3):
                subscription = UserPayments(user_id=self.user_id, order_no=self.order_no, order_amount=monthly_payment)
                pay = subscription.make_payment()
                time.sleep(3)
                if pay == False:
                    return
                else:
                    self.print_invoice()


    def refunds(self):
        def if_order_exist():
            try:
                with open(payment_book) as file:
                    payment_info = json.load(file)
                    for item in payment_info:
                        if item['order_no'] == self.order_no:
                            return True
                        else:
                            return False
            except FileNotFoundError:
                return False

        print('Hi, Welcome to Our Customer service, We apologize for any inconvienience our product must have cost you.')
        print('All Refund request takes 7 working days to fullfilled, This interval will give us an ample opportunity to investigate what went wrong so we could serve you better in the future')
        time.sleep(7)
        if if_order_exist():
            print('Hi, Thanks for your continous patronage, Your refunds has been processed, Please check your account information for your balance')
            refund_payment = UserPayments(user_id=self.user_id, order_no=self.order_no, order_amount=self.order_amount)
            refund_amount = refund_payment.order_amount


            with open(data_book) as file:
                update_user_balance = json.load(file)

                for x in range(len(update_user_balance)):
                    if update_user_balance[x]['user_id'] == self.user_id:
                        print('Old User Balance: ', update_user_balance[x]['balance'])
                        time.sleep(2)
                        update_user_balance[x]['balance'] += refund_amount 
                        print('New User Balance',update_user_balance[x]['balance'])

                with open(data_book, 'w') as file:
                    json.dump(update_user_balance,
                                file,
                                indent=4,
                                separators=(',', ':'))
                    print('Successful')
        else:
            print('Hi, After going through our records, It seems you didnt complete your order!')
            time.sleep(1)

    def print_invoice(self):
        invoice = {}
        with open(data_book) as file:
            user_info = json.load(file)
            for item in user_info:
                if item['user_id'] == self.user_id:
                    invoice['full_name'] = item['full_name']
                    invoice['amount'] = self.order_amount
                    invoice['order_no'] = self.order_no
                    invoice['order_date'] = dt.datetime.now().date().today()
        print(f'''
##########################################################################
    Thanks for Using Our Services
    Here is your invoice for Order Number {invoice["order_no"]}

    Full Name: {invoice["full_name"].title()}
    Total Amount: ${invoice["amount"]}
    Date Ordered: {invoice["order_date"]}

    Have a lovely Day
##########################################################################
        ''')
        
class PayPal:
    def __init__(self, user_id, username, order_no, order_amount):
            #TODO Check if user has card saved already.
            self.user_id = user_id
            self.username = username
            self.order_no = order_no
            self.order_amount = order_amount

            prompt = input('Type "S" to Signup for a paypal account or Type "L" to login into an existing one: ').lower()
            if prompt == 's':
                self.paypal_signup()

            elif prompt == 'l':
                self.paypal_login()

    def proceed(self):
        prompt = input('Is this a one time Payment or Subscription: "t" for One Time Payment, "s" for subscription or a Refund Request "r"?: ').lower()
        if prompt == 't':
            self.one_time_payments()
        elif prompt == 's':
            self.subscription_payments()
        elif prompt == 'r':
            self.refunds()

    def paypal_signup(self):
        print('Welcome to PayPal, Please Sign Up to Make your payment E A S Y')
        paypal_info = {}

        paypal_info['username'] =  input('Your PayPal username: ')
        paypal_info['password'] = input('Your PayPal Password: ')

        prompt = input('Do you want to save your login information? ').lower()
        if os.path.isfile(paypal_records):
            with open(paypal_records) as file:
                records = json.load(file)
                records.append({
                    'username': paypal_info['username'],
                    'password': paypal_info['password']
                    })
                with open(paypal_records, 'w') as file:
                    json.dump(records, file, indent=4, separators=(',',':'))

        else:
            with open(paypal_records, 'w') as file:
                json.dump([{
                    'username': paypal_info['username'],
                    'password': paypal_info['password']
                }], file, indent=4, separators=(',',':'))

        print('Login Successful!')
        self.proceed()

    def paypal_login(self):
        if os.path.isfile(paypal_records) is False:
            self.paypal_signup()
        else:
            print('Hi, Welcome back! Spend wisely')
            username =  input('Your PayPal username: ').lower()
            password = input('Your PayPal Password: ').lower()

            with open(paypal_records) as file:
                records = json.load(file)
                for x in range(len(records)):
                    if records[x]['username'] == username and records[x]['password'] == password:
                        print('Login Successful!')
                        self.proceed()
                        return

                    else:
                        print('Wrong username or password')    
                        return

    def one_time_payments(self):
        user_payment = UserPayments(self.user_id, self.order_no, self.order_amount)
        pay = user_payment.make_payment()
        if pay == False:
            return
        else:
            self.print_invoice()

    def subscription_payments(self):
        user_payment = UserPayments(self.user_id, self.order_no, self.order_amount)
        print('Subscription payments are timedbased, so you will be charged every 30Days (3s) for the next 90Days')
        time.sleep(1)
        prompt = input('Type "y" to proceed ').lower()
        if prompt == 'y':
            total_order = user_payment.order_amount
            monthly_payment = int(total_order/3)
            self.order_amount = monthly_payment
            for x in range(3):
                subscription = UserPayments(user_id=self.user_id, order_no=self.order_no, order_amount=monthly_payment)
                pay = subscription.make_payment()
                time.sleep(3)
                if pay == False:
                    return
                else:
                    self.print_invoice()


    def refunds(self):
        def if_order_exist():
            try:
                with open(payment_book) as file:
                    payment_info = json.load(file)
                    for item in payment_info:
                        if item['order_no'] == self.order_no:
                            return True
                        else:
                            return False
            except FileNotFoundError:
                return False

        print('Hi, Welcome to Our Customer service, We apologize for any inconvienience our product must have cost you.')
        print('All Refund request takes 7 working days to fullfilled, This interval will give us an ample opportunity to investigate what went wrong so we could serve you better in the future')
        time.sleep(7)
        if if_order_exist():
            print('Hi, Thanks for your continous patronage, Your refunds has been processed, Please check your account information for your balance')
            refund_payment = UserPayments(user_id=self.user_id, order_no=self.order_no, order_amount=self.order_amount)
            refund_amount = refund_payment.order_amount


            with open(data_book) as file:
                update_user_balance = json.load(file)

                for x in range(len(update_user_balance)):
                    if update_user_balance[x]['user_id'] == self.user_id:
                        print('Old User Balance: ', update_user_balance[x]['balance'])
                        time.sleep(2)
                        update_user_balance[x]['balance'] += refund_amount 
                        print('New User Balance',update_user_balance[x]['balance'])

                with open(data_book, 'w') as file:
                    json.dump(update_user_balance,
                                file,
                                indent=4,
                                separators=(',', ':'))
                    print('Successful')
        else:
            print('Hi, After going through our records, It seems you didnt complete your order!')
            time.sleep(1)

    def print_invoice(self):
        invoice = {}
        with open(data_book) as file:
            user_info = json.load(file)
            for item in user_info:
                if item['user_id'] == self.user_id:
                    invoice['full_name'] = item['full_name']
                    invoice['amount'] = self.order_amount
                    invoice['order_no'] = self.order_no
                    invoice['order_date'] = dt.datetime.now().date().today()
        print(f'''
##########################################################################
    Thanks for Using Our Services
    Here is your invoice for Order Number {invoice["order_no"]}

    Full Name: {invoice["full_name"].title()}
    Total Amount: ${invoice["amount"]}
    Date Ordered: {invoice["order_date"]}

    Have a lovely Day
##########################################################################
        ''')

class Bank:
    def __init__(self, user_id, order_amount, order_no):
        self.user_id = user_id
        self.order_amount = order_amount
        self.order_no = order_no
        self.proceed()

    def proceed(self):
        prompt = input('Is this a one time Payment or Subscription: "t" for One Time Payment, "s" for subscription or a Refund Request "r"?: ').lower()
        if prompt == 't':
            self.one_time_payments()
        elif prompt == 's':
            self.subscription_payments()
        elif prompt == 'r':
            self.refunds()

    def one_time_payments(self):
        user_payment = UserPayments(self.user_id, self.order_no, self.order_amount)
        pay = user_payment.make_payment()
        # Checks wheter the payment bounced due to Insufficient funds
        if pay == False:
            return
        else:
            self.print_invoice()

    def subscription_payments(self):
        user_payment = UserPayments(self.user_id, self.order_no, self.order_amount)
        print('Subscription payments are timedbased, so you will be charged every 30Days (3s) for the next 90Days')
        time.sleep(1)
        prompt = input('Type "y" to proceed ').lower()
        if prompt == 'y':
            total_order = user_payment.order_amount
            monthly_payment = int(total_order/3)
            self.order_amount = monthly_payment
            for x in range(3):
                subscription = UserPayments(user_id=self.user_id, order_no=self.order_no, order_amount=monthly_payment)
                pay = subscription.make_payment()
                time.sleep(3)
                if pay == False:
                    return
                else:
                    self.print_invoice()

    def refunds(self):
        def if_order_exist():
                try:
                    with open(payment_book) as file:
                        payment_info = json.load(file)
                        for item in payment_info:
                            if item['order_no'] == self.order_no:
                                return True
                            else:
                                return False
                except FileNotFoundError:
                    return False

        print('Hi, Welcome to Our Customer service, We apologize for any inconvienience our product must have cost you.')
        print('All Refund request takes 7 working days to fullfilled, This interval will give us an ample opportunity to investigate what went wrong so we could serve you better in the future')
        time.sleep(7)
        if if_order_exist():
            print('Hi, Thanks for your continous patronage, Your refunds has been processed, Please check your account information for your balance')
            refund_payment = UserPayments(user_id=self.user_id, order_no=self.order_no, order_amount=self.order_amount)
            refund_amount = refund_payment.order_amount


            with open(data_book) as file:
                update_user_balance = json.load(file)

                for x in range(len(update_user_balance)):
                    if update_user_balance[x]['user_id'] == self.user_id:
                        print('Old User Balance: ', update_user_balance[x]['balance'])
                        time.sleep(2)
                        update_user_balance[x]['balance'] += refund_amount 
                        print('New User Balance',update_user_balance[x]['balance'])

                with open(data_book, 'w') as file:
                    json.dump(update_user_balance,
                                file,
                                indent=4,
                                separators=(',', ':'))
                    print('Successful')
        else:
            print('Hi, After going through our records, It seems you didnt complete your order!')
            time.sleep(1)

    def print_invoice(self):
        invoice = {}
        with open(data_book) as file:
            user_info = json.load(file)
            for item in user_info:
                if item['user_id'] == self.user_id:
                    invoice['full_name'] = item['full_name']
                    invoice['amount'] = self.order_amount
                    invoice['order_no'] = self.order_no
                    invoice['order_date'] = dt.datetime.now().date().today()
        print(f'''
##########################################################################
    Thanks for Using Our Services
    Here is your invoice for Order Number {invoice["order_no"]}

    Full Name: {invoice["full_name"].title()}
    Total Amount: ${invoice["amount"]}
    Date Ordered: {invoice["order_date"]}

    Have a lovely Day
##########################################################################
        ''')