import enum
from user import User
import random

class Transactions(User):
    def __init__(self, id, amount):
        self.id = id
        self.confirmation_code = random.randint(1000, 9999)
        self.user = self.username
        self.amount = amount
        self.status = ['pending', 'paid', 'cancelled']

