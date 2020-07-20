# import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
    )
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
    )

    def post(self):

        data = UserRegister.parser.parse_args()

        # db_name = "C:\Users\Vivekananda Reddy\PycharmProjects\Gaju_Flask-Section5\code\data.db"

        if UserModel.find_by_username(data["username"]):
            return {"message": "A user with this name already exists."}, 400

        # connection = sqlite3.connect("my_data.db")
        # cursor = connection.cursor()
        #
        # insert_query = "INSERT INTO users VALUES (NULL, ?, ?)"
        # cursor.execute(insert_query, (data["username"], data["password"]))
        #
        # connection.commit()
        # connection.close()

        user = UserModel(**data)  # UserModel(data["username"],data["password"])
        user.save_to_db()

        return {"message": "user created successfully."}, 201