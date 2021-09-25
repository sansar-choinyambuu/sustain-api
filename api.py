from flask import Flask, request, jsonify
from flask_restx import Resource, Api, reqparse
import json

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="Sustainability API",
    description="REST API that provides sustainability score for customer/cart/product",
)
api.namespaces.clear()
score_ns = api.namespace("score", description="Sustainability score")
product_ns = api.namespace("product", description="Product and Recommendations")

customers = {
    "cus1": {"name": "Sansar", "age": 34, "score": 100, "carts": ["cart1", "cart2"]},
    "cus2": {"name": "Angela", "age": 80, "score": 20, "carts": ["cart3"]},
}
cart = {
    "cart1": {"products": [{"name": "tomato", "score": 10}, {"name": "eggs", "score": 20}], "score": 10},
    "cart2": {"products": [{"name": "schoggi", "score": 0}, {"name": "onion", "score": 5}], "score": 16},
    "cart3": {"products": [{"name": "flour", "score": 2}, {"name": "vanilla", "score": 30}], "score": 88},
}

product = {
    "prod1": {"name": "egg", "score": 20},
    "prod2": {"name": "tomato", "score": 10},
    "prod3": {"name": "flour", "score": 2}
}

customer_parser = reqparse.RequestParser()
customer_parser.add_argument("customer_id", type=str, required=True, help="Customer ID")

cart_parser = reqparse.RequestParser()
cart_parser.add_argument("cart_id", type=str, required=True, help="Shopping Cart ID")

product_parser = reqparse.RequestParser()
product_parser.add_argument("product_id", type=str, required=True, help="Product ID")


@score_ns.route("/customer")
@score_ns.expect(customer_parser)
class Customer(Resource):
    def get(self):
        args = request.args
        customer_id = args["customer_id"]
        return jsonify(customers[customer_id])

@score_ns.route("/cart")
@score_ns.expect(cart_parser)
class Cart(Resource):
    def get(self):
        args = request.args
        cart_id = args["cart_id"]
        return jsonify(cart[cart_id])

@product_ns.route("/recommendation")
@product_ns.expect(product_parser)
class Recommendation(Resource):
    def get(self):
        args = request.args
        product_id = args["product_id"]
        return jsonify(["Don't buy the product"])

@product_ns.route("/info")
@product_ns.expect(product_parser)
class ProductInfo(Resource):
    def get(self):
        args = request.args
        product_id = args["product_id"]
        return jsonify(product[product_id])


api.add_resource(Customer, "/customer")
api.add_resource(Cart, "/cart")
api.add_resource(Recommendation, "/recommendation")

if __name__ == "__main__":
    app.run(debug=True)
