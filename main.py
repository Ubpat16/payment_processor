from user import User
from transaction import Transactions

user = User(id=1, username='poly', first_name='ubon', last_name='okon', full_name='ubon patrusm okon', pending_transactions=None, paid_transactions=None, total_paid_amount=None)
user_transaction = Transactions(id=1, amount=5000)
print(user_transaction.confirmation_code)