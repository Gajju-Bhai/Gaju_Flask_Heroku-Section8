from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)
# import sqlite3
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
    )
    parser.add_argument("store_id",
                        type=int,
                        required=True,
                        help="Every item needs a store id."
    )

    @jwt_required
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.json()

        return {"message": "Item not found"}, 404

    @fresh_jwt_required
    def post(self, name):
        if ItemModel.find_item_by_name(name):
            return {"message": "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        # item = ItemModel(name,data["price"],data["store_id"])
        item = ItemModel(name, **data)

        try:
            #item.insert()
            item.save_to_db()
        except Exception as e:
            print(str(e))
            return {"message": "An error occurred while inserting the item."}, 500 # Internal server error

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        # connection = sqlite3.connect("my_data.db")
        # cursor = connection.cursor()
        #
        # delete_query = "DELETE FROM items WHERE name=?"
        # cursor.execute(delete_query, (name,))
        # connection.commit()
        # connection.close()
        # return {"message": "item deleted"}

        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"message": "Admin privilege required."}, 401
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item is deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_item_by_name(name)
        #new_item = ItemModel(name, data["price"])
        if item is None:
            # try:
            #     new_item.insert()
            # except:
            #     return {"message": "An error occurred while updating and inserting the item"}, 500
            # item = ItemModel(name, data["price"],data["store_id"])
            item = ItemModel(name, **data)
        else:
            #new_item.update()
            item.price = data["price"]
            # item.store_id = data["store_id"]

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @jwt_optional
    def get(self):
        # connection = sqlite3.connect("my_data.db")
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items_list = []
        #
        # for row in result:
        #     items_list.append({"name": row[1], "price": row[2]})
        #
        # connection.close()
        #
        # return {"items": items_list}

        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {
                   'items': [item['name'] for item in items],
                   'message': 'More data available if you log in.'
               }, 200

        # return {"items": list(map(lambda x:x.json(), ItemModel.query.all()))}
        # return {"items": [item.json() for item in ItemModel.find_all()]}
