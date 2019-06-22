from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from classlib.users import User


class UsersRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='Must supply a username.'
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='Must supply a password.'
                        )

    def get(self):
        data = UsersRegister.parser.parse_args()
        user = User(**data)
        user = user.get_by_username(user.username)
        if user:
            return user.json(), 201
        return {'message': 'User not found.'}

    def post(self):
        data = UsersRegister.parser.parse_args()

        if User.get_by_username(data['username']):
            return {'message': 'Username already exists.'}, 400

        user = User(**data)
        user.add_user()
        return user.json(), 201

    @jwt_required()
    def delete(self):
        data = UsersRegister.parser.parse_args()
        user = User.get_by_username(data['username'])
        print(user.json())
        if user:
            if user.password == data['password']:
                user.del_user()
                return user.json()
            return {'message': 'Incorrect password.'}, 400
        return {'message': 'User not found.'}, 404
