from app import bcrypt
from datetime import datetime, timedelta, timezone

loans = {}
users = {}
repayments = {}

loan_counter = 1
repayment_counter = 1

class User:
    def __init__(self, username, password_hash):
        self.id = len(users) + 1
        self.username = username
        self.password_hash = password_hash
        self.loans = []

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Loan:
    def __init__(self, amount, term, user_id):
        global loan_counter
        self.id = loan_counter
        loan_counter += 1
        self.amount = amount
        self.term = term
        self.start_date = datetime.now(timezone.utc)
        self.status = 'PENDING'
        self.user_id = user_id
        self.repayments = []
        self.schedule_repayments()

    def schedule_repayments(self):
        global repayment_counter
        weekly_amount = round(self.amount / self.term, 2)
        for week in range(1, self.term + 1):
            repayment_date = self.start_date + timedelta(weeks=week)
            repayment = Repayment(
                amount=weekly_amount,
                due_date=repayment_date,
                status='PENDING',
                loan_id=self.id
            )
            repayment.id = repayment_counter
            repayment_counter += 1
            self.repayments.append(repayment.id)
            repayments[repayment.id] = repayment

class Repayment:
    def __init__(self, amount, due_date, status, loan_id):
        self.id = None
        self.amount = amount
        self.due_date = due_date
        self.status = status
        self.loan_id = loan_id
