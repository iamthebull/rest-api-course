import os

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.users import UsersRegister
from auth import authenticate, identity

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = 'secretkey'
jwt = JWT(app, authenticate, identity)

api = Api(app)
api.add_resource(UsersRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
