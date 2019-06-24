from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                get_jwt_claims,
                                get_jwt_identity,
                                jwt_optional,
                                jwt_refresh_token_required,
                                jwt_required
                                )
from flask_restful import Resource, reqparse

from classlib.users import User

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help='Must supply a username.'
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help='Must supply a password.'
                          )


class UsersRegister(Resource):

    def get(self):
        data = _user_parser.parse_args()
        user = User(**data)
        user = user.get_by_username(user.username)
        if user:
            return user.json(), 201
        return {'message': 'User not found.'}

    def post(self):
        data = _user_parser.parse_args()

        if User.get_by_username(data['username']):
            return {'message': 'Username already exists.'}, 400

        user = User(**data)
        user.add_user()
        return user.json(), 201

    @jwt_required
    def delete(self):
        data = _user_parser.parse_args()
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required to delete.'}
        user = User.get_by_username(data['username'])
        if user:
            if user.password == data['password']:
                user.del_user()
                return user.json()
            return {'message': 'Incorrect password.'}, 400
        return {'message': 'User not found.'}, 404


class AllUsers(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        if user_id:
            return {'Users': [user.json() for user in User.get_all()]}, 200
        return {'Users': [user.username for user in User.get_all()],
                'message': 'More detail available if you log in.'}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = User.get_by_username(data['username'])

        if user and user.password == data['password']:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {'access_token': access_token, 'refresh_token': refresh_token}, 200
        return {'message': 'Invalid credentials.'}, 401


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
