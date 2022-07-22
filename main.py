from transaction import Transactions
from user import User
import os

app_data = 'appdata'
if os.path.isdir(app_data):
    pass
else:
    os.mkdir('appdata')

user = User(id=1,
            username='poly',
            first_name='ubon',
            last_name='okon',
            full_name='ubon patrusm okon')

user.save_user()

user_transaction = Transactions(id=1, user='poly')
pay = user_transaction.place_order(id=1, user='poly')
