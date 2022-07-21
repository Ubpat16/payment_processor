class Transactions:
    def __init__(self, id, confirmation_code, user, amount, status=enumerate('pending', 'paid', 'cancelled')):
        self.id = id
        self.confirmation_code = confirmation_code
        self.user = user
        self.amount = amount
        self.status = status
