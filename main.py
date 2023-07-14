from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Create an instance of the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

# Create a model for the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        self.name = name

# Create a schema for serialization/deserialization
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Define a resource for user operations
class UserResource(Resource):
    def get(self, user_id=None):
        if user_id is not None:
            user = User.query.get(user_id)
            if user:
                return jsonify(user_schema.dump(user))
            else:
                return jsonify({'message': 'User not found'}), 404
        else:
            users = User.query.all()
            return jsonify(users_schema.dump(users))

    def post(self):
        name = request.json['name']
        new_user = User(name)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(user_schema.dump(new_user)), 201

    def put(self, user_id):
        user = User.query.get(user_id)
        if user:
            name = request.json['name']
            user.name = name
            db.session.commit()
            return jsonify(user_schema.dump(user))
        else:
            return jsonify({'message': 'User not found'}), 404

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return '', 204
        else:
            return jsonify({'message': 'User not found'}), 404

# Define routes for user resource
api.add_resource(UserResource, '/api/users', '/api/users/<int:user_id>')

# Run the Flask app
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
