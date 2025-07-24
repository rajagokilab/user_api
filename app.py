from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from data import users, user_id_counter

app = Flask(__name__)
api = Api(app)

class UserList(Resource):
    def get(self):
        return jsonify(users)

    def post(self):
        global user_id_counter
        data = request.get_json()
        new_user = {
            'id': user_id_counter,
            'name': data.get('name'),
            'email': data.get('email')
        }
        users.append(new_user)
        user_id_counter += 1
        return new_user, 201

class User(Resource):
    def get(self, id):
        user = next((u for u in users if u['id'] == id), None)
        if user:
            return user
        return {'message': 'User not found'}, 404

    def put(self, id):
        data = request.get_json()
        user = next((u for u in users if u['id'] == id), None)
        if user:
            user.update({
                'name': data.get('name', user['name']),
                'email': data.get('email', user['email'])
            })
            return user
        return {'message': 'User not found'}, 404

    def delete(self, id):
        global users
        user = next((u for u in users if u['id'] == id), None)
        if user:
            users = [u for u in users if u['id'] != id]
            return {'message': 'User deleted'}
        return {'message': 'User not found'}, 404

api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
