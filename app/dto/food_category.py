from flask_restx import Namespace, fields


class FoodCategoryDto:
    api = Namespace("FoodCategory",  description="Api food place document")

    food_category_field = api.model('FoodCategory', {
        "_id": fields.String(),
        "oldDishTypeID": fields.String(),
        "foodPlaceID": fields.String(),
        "createTime": fields.String()
    })