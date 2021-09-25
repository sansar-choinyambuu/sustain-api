from flask import Flask, request, jsonify, Response
from flask_restx import Resource, Api, reqparse
import json
import pymongo
from mongo import Mongo

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="Sustainability API",
    description="REST API that provides sustainability score for customer/cart/product and recommends more sustainable product options",
)
api.namespaces.clear()
score_ns = api.namespace("score", description="Sustainability score")
product_ns = api.namespace("product", description="Product and Recommendations")

mongo = Mongo()

product = {
    "prod1": {"name": "egg", "score": 20},
    "prod2": {"name": "tomato", "score": 10},
    "prod3": {"name": "flour", "score": 2}
}

customer_parser = reqparse.RequestParser()
customer_parser.add_argument("customer_id", type=str, required=True, help="Customer ID")

product_parser = reqparse.RequestParser()
product_parser.add_argument("product_id", type=str, required=True, help="Product ID")

@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

# Returns all purchases for a customer id
@score_ns.route("/customer")
@score_ns.expect(customer_parser)
class Customer(Resource):
    def get(self):
        args = request.args
        customer_id = args["customer_id"]
        return jsonify(mongo.get_customer(customer_id))

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
api.add_resource(Recommendation, "/recommendation")

if __name__ == "__main__":
    app.run(debug=True)
