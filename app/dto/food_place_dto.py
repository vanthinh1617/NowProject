from flask_restx import Namespace, fields

class FoodPlaceDto:
    api = Namespace("FoodPlace",  description="Api food place document",)
    
    food_place_fields= api.model("FoodPlaceModel", {
        "_id": fields.String(),
        "userID": fields.String(),
        "name": fields.String(),
        "nameWithoutAccent": fields.String(),
        "amenities": fields.String(),
        "phone": fields.String(),
        "email": fields.String(),
        "website": fields.String(),
        "maxPrice": fields.Integer(),
        "minPrice": fields.Integer(),
        "allowView": fields.Integer(),
        "status": fields.Integer(),
        "avgRating": fields.Integer(),
        "totalReview": fields.Integer(),
        "createTime":  fields.String(),
    })

    food_place = api.model('FoodPlace', {
        'data': fields.Nested(food_place_fields),
        'statusCode': fields.Integer(required=True, description='response status code'),
        'message': fields.String(required=True, description='response code')
    })

