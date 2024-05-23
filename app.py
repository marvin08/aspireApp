from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from routes import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aspireApp_secret_key'
app.config['JWT_SECRET_KEY'] = 'aspireApp_jwt_secret_key'

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(debug=False)
