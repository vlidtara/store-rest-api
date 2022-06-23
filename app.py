from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from resources.users import Register, User, Users
from resources.items import Item, Items
from resources.store import Store, StoreList
from resources.greeting import Greeting

from datetime import timedelta
from security import authenticate, identity as identity_function
import os

try:
    uri = os.getenv("DATABASE_URL")  # or other relevant config var
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
except:
    pass

app = Flask(__name__)
app.secret_key = "skdnmlcnevnle332d2"
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = uri if uri else 'sqlite:///mydata.db'
jwt = JWT(app, authenticate, identity_function)


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })


@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code
    }), error.status_code


api = Api(app)

api.add_resource(Greeting, "/")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(Items, "/items")
api.add_resource(Register, "/register")
api.add_resource(User, "/user/<int:id>")
api.add_resource(Users, "/users")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run()
