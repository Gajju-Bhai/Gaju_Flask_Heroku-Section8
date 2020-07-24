import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister, User
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///my_data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = "vivek"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

# class Student(Resource):
#     def get(self,name):
#         return {'student': name}
#
# api.add_resource(Student, '/student/<string:name>')   # http://127.0.0.1:5000/student/Vivek

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=4999, debug=True)