import pymongo
from bson.json_util import dumps
from bson.json_util import loads
from functools import reduce


URI = "mongodb+srv://sustain:sustain@cluster0.rmjhl.mongodb.net/sustaindb?retryWrites=true&w=majority"
DB = "sustaindb"
CUSTOMER_COL = "customers"
PRODUCT_COL = "products"

CARBON_FOOTPRINT_RATING_PATH = "m_check2.carbon_footprint.ground_and_sea_cargo.rating"
ANIMAL_WELFARE_RATING_PATH = "m_check2.animal_welfare.rating"


class Mongo:
    def __init__(self, uri=URI):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[DB]

        self.products = self.__find__(
            PRODUCT_COL,
            {},
            {
                "id": 1,
                "name": 1,
                "image.original": 1,
                "image.stack": 1,
                CARBON_FOOTPRINT_RATING_PATH: 1,
                ANIMAL_WELFARE_RATING_PATH: 1,
            },
        )
        self.products = loads(dumps(self.products))
        self.products = {
            p["id"]: {
                "name": p["name"],
                "image": p["image"]["original"],
                "image_stack": p["image"]["stack"],
                "climate_rating": self.__deep_get_score(
                    p, CARBON_FOOTPRINT_RATING_PATH
                ),
                "animalwelfare_rating": self.__deep_get_score(
                    p, ANIMAL_WELFARE_RATING_PATH
                ),
            }
            for p in self.products
        }

    def __deep_get_score(self, dictionary, keys, default=0):
        return reduce(
            lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
            keys.split("."),
            dictionary,
        )

    def __find__(self, collection, query, projection=None):
        col = self.db[collection]
        return col.find(query, projection)

    def __find_one__(self, collection, query, projection=None):
        col = self.db[collection]
        return col.find_one(query, projection)

    def get_product_info(self, product_id: str):
        product = self.__find_one__(PRODUCT_COL, {"id": product_id}, {"id": 1, "name": 1, "_id": 0, "image.original": 1, "price.item.price": 1, "m_check2": 1})
        return product

    def get_recommended_info(self, product_ids):
        result = {"bad": [], "good": []}
        for item in product_ids["bad"]:
            result["bad"].append(self.get_product_info(str(item)))
        for item in product_ids["good"]:
            result["good"].append(self.get_product_info(str(item)))

        return result

    def get_customer(self, customer_id: str, last_n=5):
        customer = self.__find_one__(CUSTOMER_COL, {"id": customer_id})
        ret = {"id": customer["id"]}
        ret["purchases"] = [
            {"unix_timestamp": p["unix_timestamp"], "products": p["products"]}
            for p in customer["purchases"][:last_n]
        ]

        # retrieve sustainability scores for all products in purchases
        for purchase in ret["purchases"]:
            purchase["products"] = [
                {
                    **p,
                    **{
                        "climate_rating": self.products[p["product_id"]][
                            "climate_rating"
                        ],
                        "animalwelfare_rating": self.products[p["product_id"]][
                            "animalwelfare_rating"
                        ],
                        "name": self.products[p["product_id"]]["name"]
                    },
                }
                for p in purchase["products"]
                if p["product_id"] in self.products
            ]

        # calculate sustainability score for customer, purchase
        for purchase in ret["purchases"]:
            amount_sum = sum(float(p["amount"]) for p in purchase["products"])
            climate_score_sum = sum(
                float(p["amount"]) * p["climate_rating"] for p in purchase["products"]
            )
            animalwelfare_score_sum = sum(
                float(p["amount"]) * p["animalwelfare_rating"]
                for p in purchase["products"]
            )

            purchase["climate_score"] = climate_score_sum / amount_sum
            purchase["animalwelfare_score"] = animalwelfare_score_sum / amount_sum

        
        ret["climate_score"] = sum(p["climate_score"] for p in ret["purchases"]) / len(ret["purchases"])
        ret["animalwelfare_score"] = sum(p["animalwelfare_score"] for p in ret["purchases"]) / len(ret["purchases"])

        return ret


if __name__ == "__main__":
    d = Mongo()
    print(d.products["100100300000"])
    print(d.get_customer("100688"))

