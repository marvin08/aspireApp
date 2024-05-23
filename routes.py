from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import app
from models import users, loans, repayments, User, Loan

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users:
        return jsonify({"message": "User already exists in the system"}), 400

    new_user = User(username=username, password_hash=None)
    new_user.set_password(password)
    users[username] = new_user

    return jsonify({"message": "User has been registered successfully!"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users.get(username)
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"message": "Invalid creds for the User!"}), 401

@app.route('/loan', methods=['POST'])
@jwt_required()
def create_loan():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    amount = data.get('amount')
    term = data.get('term')

    new_loan = Loan(amount=amount, term=term, user_id=current_user_id)
    loans[new_loan.id] = new_loan
    users[current_user_id].loans.append(new_loan.id)

    return jsonify({"message": "Loan has been added successfully!"}), 201

@app.route('/loan/<int:loan_id>', methods=['GET'])
@jwt_required()
def view_loan(loan_id):
    current_user_id = get_jwt_identity()
    loan = loans.get(loan_id)

    if loan.user_id != current_user_id:
        return jsonify({"message": "Access denied!"}), 403

    repayments_list = [
        {"id": r.id, "amount": r.amount, "due_date": r.due_date, "status": r.status} for r in [repayments[rep_id] for rep_id in loan.repayments]
    ]

    return jsonify({
        "id": loan.id,
        "amount": loan.amount,
        "term": loan.term,
        "status": loan.status,
        "repayments": repayments_list
    }), 200

@app.route('/loan/<int:loan_id>/approve', methods=['POST'])
@jwt_required()
def approve_loan(loan_id):
    # Assuming the current user is an admin for simplicity
    loan = loans.get(loan_id)
    loan.status = 'APPROVED'

    return jsonify({"message": "Loan has been approved successfully!"}), 200

@app.route('/repayment', methods=['POST'])
@jwt_required()
def repay():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    repayment_id = data.get('repayment_id')
    amount = data.get('amount')

    repayment = repayments.get(repayment_id)
    loan = loans.get(repayment.loan_id)

    if loan.user_id != current_user_id:
        return jsonify({"message": "Access denied!"}), 403

    if amount >= repayment.amount:
        repayment.status = 'PAID'

        # Check if all repayments are paid
        if all(repayments[rep_id].status == 'PAID' for rep_id in loan.repayments):
            loan.status = 'PAID'

        return jsonify({"message": "Repayment is successful!"}), 200

    return jsonify({"message": "Insufficient amount to repay!"}), 400
