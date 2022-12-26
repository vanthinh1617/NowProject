from flask_restx import Namespace, fields
class FoodPlaceDto:
    api = Namespace("FoodPlace",  description="Api food place document",)
    
    day_of_week_fields =  api.model(name="TimeFields",model= {
                                "OPEN": fields.Integer,
                                "CLOSE": fields.Integer
                                })
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
        "openTimes": fields.Nested(api.model(name="DaysOfWeekFields",model= {
                                "MONDAY": fields.List(fields.Nested(day_of_week_fields)),
                                "TUESDAY": fields.List(fields.Nested(day_of_week_fields)),
                                "WEDNESDAY":  fields.List(fields.Nested(day_of_week_fields)),
                                "THURSDAY":  fields.List(fields.Nested(day_of_week_fields)),
                                "FRIDAY":  fields.List(fields.Nested(day_of_week_fields)),
                                "SATURDAY":  fields.List(fields.Nested(day_of_week_fields)),
                                "SUNDAY":  fields.List(fields.Nested(day_of_week_fields))
                            })),
        "createTime":  fields.String(),
    })

    food_place = api.model('FoodPlace', {
        'data': fields.Nested(food_place_fields),
        'statusCode': fields.Integer(required=True, description='response status code'),
        'message': fields.String(required=True, description='response code')
    })

    food_place_create = api.model('FoodPlaceCreate',{
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
        "categories": fields.List(fields.String),
    })

