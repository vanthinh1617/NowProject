from flask_restx import Namespace, fields

class FoodTypeAndStyleDto:
    api = Namespace("FoodTypeAndStyle",  description="Api food type and style document",)

    food_type_field = api.model("FoodTypeAndStyle", {
        "_id": fields.String(),
        "foodPlaceID": fields.String(),
        "type": fields.String(),
        "dinningTimes": fields.String(),
        "price": fields.Integer(),
        "styles": fields.String(),
        "good_for": fields.String(),
        "standFood": fields.String(),
        "capacity": fields.Integer(),
        "lastAdmissionTime": fields.String(),
        "preparationTime": fields.String(),
        "holiday": fields.String()
    })