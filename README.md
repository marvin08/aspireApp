
# Loan Application API

## Introduction
This is a REST API for a mini Aspire application system where users can request for loans, admins can approve the loans, and users can make repayments for the loans.

## Requirements
- Python 3.8+
- Flask
- Flask-Bcrypt
- Flask-JWT-Extended

## Setup

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd loan_app
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   flask run
   ```

## API Endpoints

### User Registration
- **URL**: /register
- **Method**: POST
- **Description**: Register a new user.
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Responses**:
  - `201 Created`: User created successfully.
  - `400 Bad Request`: User already exists.

### User Login
- **URL**: /login
- **Method**: POST
- **Description**: Login and get a JWT token.
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Responses**:
  - `200 OK`: Returns JWT token.
  - `401 Unauthorized`: Invalid credentials.

### Create Loan
- **URL**: /loan
- **Method**: POST
- **Description**: Create a new loan (Authenticated users).
- **Headers**:
  - `Authorization`: Bearer <JWT Token>
- **Request Body**:
  ```json
  {
    "amount": "float",
    "term": "int"
  }
  ```
- **Responses**:
  - `201 Created`: Loan created successfully.

### View Loan
- **URL**: /loan/<loan_id>
- **Method**: GET
- **Description**: View a specific loan (Authenticated users).
- **Headers**:
  - `Authorization`: Bearer <JWT Token>
- **Responses**:
  - `200 OK`: Returns loan details.
  - `403 Forbidden`: Access forbidden (not the loan owner).

### Approve Loan
- **URL**: /loan/<loan_id>/approve
- **Method**: POST
- **Description**: Approve a loan (Assuming admin functionality).
- **Headers**:
  - `Authorization`: Bearer <JWT Token>
- **Responses**:
  - `200 OK`: Loan approved successfully.

### Make Repayment
- **URL**: /repayment
- **Method**: POST
- **Description**: Make a repayment (Authenticated users).
- **Headers**:
  - `Authorization`: Bearer <JWT Token>
- **Request Body**:
  ```json
  {
    "repayment_id": "int",
    "amount": "float"
  }
  ```
- **Responses**:
  - `200 OK`: Repayment successful.
  - `403 Forbidden`: Access forbidden (not the loan owner).
  - `400 Bad Request`: Insufficient repayment amount.

## Running Tests

Run the tests using:
```bash
python -m unittest discover tests
```

## Notes

- This application uses in-memory storage, meaning all data will be lost when the server is restarted.
- The application assumes a simplistic admin functionality for approving loans. In a real-world application, a more robust user role management system would be implemented.
- The `@jwt_required()` decorator is used to secure endpoints, ensuring only authenticated users can access certain routes.
