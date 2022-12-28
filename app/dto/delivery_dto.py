from flask_restx import Namespace, fields


class DeliveryDto:
    api = Namespace("Delivery",  description="Api user client",)

    search_global_field = api.model("Search global field", {
        "cityID": fields.Integer(),
        "combineCategories": fields.Integer()
    })
