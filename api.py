from flask import Flask, request, jsonify
from flask_restx import Resource, Api, reqparse
import json

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="Sustainability API",
    description="REST API that provides sustainability scores for customer/carts/products",
)
api.namespaces.clear()
ns = api.namespace("", description="Get sustainability scores for customer/carts/products")

customers = {
    "cus1": {"name": "Sansar", "age": 34, "score": 100},
    "cus2": {"name": "Angela", "age": 80, "score": 20},
}
carts = {
    "cus1-cart1": {"items": [{"name": "tomato", "score": 10}, {"name": "eggs", "score": 20}], "score": 10},
    "cus1-cart2": {"items": [{"name": "schoggi", "score": 0}, {"name": "onion", "score": 5}], "score": 16},
    "cus2-cart1": {"items": [{"name": "flour", "score": 2}, {"name": "vanilla", "score": 30}], "score": 88},
}


customer_parser = reqparse.RequestParser()
customer_parser.add_argument("customer_id", type=str, required=True, help="Customer ID")

cart_parser = reqparse.RequestParser()
cart_parser.add_argument("customer_id", type=str, required=True, help="Customer ID")
cart_parser.add_argument("cart_id", type=str, required=True, help="Shopping Cart ID")


@ns.route("/customer")
@ns.expect(customer_parser)
class Customer(Resource):
    def get(self):
        args = request.args
        customer_id = args["customer_id"]
        return jsonify(customers[customer_id])

@ns.route("/cart")
@ns.expect(cart_parser)
class Cart(Resource):
    def get(self):
        args = request.args
        customer_id = args["customer_id"]
        cart_id = args["cart_id"]
        return jsonify(carts[str.format(f"{customer_id}-{cart_id}")])


api.add_resource(Customer, "/customer")
api.add_resource(Cart, "/cart")

if __name__ == "__main__":
    app.run(debug=True)
