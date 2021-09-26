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

recommendations ={
    "meat": {"bad": [232102082000, 220220040000, 241110501000], "good": [241102765000, 220220030020, 232300185300]},
    "dairy": {"bad": [204105600000, 210401724000, 205008000000], "good": [205050100000, 210404024000, 204104300200]}
}

customer_parser = reqparse.RequestParser()
customer_parser.add_argument("customer_id", type=str, required=True, help="Customer ID [e.g. 100688]")

customization_parser = reqparse.RequestParser()
customization_parser.add_argument("customer_id", type=str, required=True, help="Customer ID [e.g. 100688]")
customization_parser.add_argument("footprint", type=str, required=True, help="Carbon footprint")
customization_parser.add_argument("water", type=str, required=True, help="Water scarcity")
customization_parser.add_argument("animals", type=str, required=True, help="Animal welfare")

product_parser = reqparse.RequestParser()
product_parser.add_argument("product_id", type=str, required=True, help="Product ID [e.g. 100100300000]")

recommendation_parser = reqparse.RequestParser()
recommendation_parser.add_argument("category", type=str, required=True, help="Category: [meat, dairy]")

# TODO elaborate security measures

@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@score_ns.route("/customer")
@score_ns.expect(customer_parser)
class Customer(Resource):
    def get(self):
        args = request.args
        customer_id = args["customer_id"]
        return jsonify(mongo.get_customer(customer_id))

@score_ns.route("/customization")
@score_ns.expect(customization_parser)
class Customer(Resource):
    def post(self):
        # args = request.args
        # customer_id = args["customer_id"]
        return jsonify(["Totally saved all of that, trust me!"])

@product_ns.route("/recommendation")
@product_ns.expect(recommendation_parser)
class Recommendation(Resource):
    def get(self):
        args = request.args
        category_name = args["category"]
        if category_name in recommendations:
            # print(recommendations[category_name]["bad"][0])

            return jsonify(mongo.get_recommended_info(recommendations[category_name]))
            # return jsonify(recommendations[category_name])
        else:
            return jsonify(["This category does not exist!"])

@product_ns.route("/info")
@product_ns.expect(product_parser)
class ProductInfo(Resource):
    def get(self):
        args = request.args
        product_id = args["product_id"]
        return jsonify(mongo.get_product_info(product_id))


api.add_resource(Customer, "/customer")
api.add_resource(Recommendation, "/recommendation")

if __name__ == "__main__":
    app.run(debug=True)
