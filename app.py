import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from resources.users import UsersRegister, AllUsers, UserLogin

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = 'secretkey'
jwt = JWTManager(app)

api = Api(app)
api.add_resource(UsersRegister, '/register')
api.add_resource(AllUsers, '/all')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
