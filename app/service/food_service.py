from app.model.db import foodPlacesCollection, foodCategoryLangsCollection, foodCategoriesCollection
from app.model.model import FoodPlaces, Users, FoodCategories, FoodCategoriesLangs
from bson.objectid import ObjectId
from app.util.helpers import _throw
from app.util.jwt import get_current_user
from app.util.exception import NotPermissionException, NotFoundDataException
from app.service.food_type_and_style import FoodTypeAndStyleService
from flask import request
import json, os
class FoodPlaceService:
    @staticmethod
    def get_lists(page= 1, page_size = 30):
        page = int(page)
        page_size = int(page_size)
        list_food =  foodPlacesCollection.find().skip((page -1) * page_size).limit(page_size)
        return list(list_food)

    @staticmethod
    def get_by_id(id):
        lang = request.cookies.get('lang')
        result = foodPlacesCollection.aggregate([
            {"$match": {"_id": ObjectId(id)}},
            {"$lookup" : {
                "from": "foodCategories",
                "let": {"foodPlaceID": "$_id"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$eq": ["$foodPlaceID", "$$foodPlaceID"] 
                            }
                        }
                    },
                    {"$lookup" : {
                        "from": "foodCategoryLangs",
                        "let": {"categoryID": "$_id"},
                        "pipeline": [
                           { 
                                "$match": {
                                    "$expr": {
                                        "$and": [
                                            { "$eq": ["$foodCategoryID", "$$categoryID"] },
                                            {"$eq": ["$lang",lang]}
                                        ]
                                       
                                    }  
                                }
                            },
                            {"$project": {"_id": 0, "categoryName": 1,"lang": 1}}
                        ],
                        "as": "category"
                    }},
                    {"$project": {"_id": 0, "category": 1}}
                ],
                "as": "categories"
            }} 

        ])
        result = list(result)
        FoodPlaceService.assert_food_place(result)

        return result[0]

    @staticmethod
    def create(payload):
        try:
            if payload['openTimes'] != None : 
                payload['openTimes'] = json.dumps(payload['openTimes'])


            food = FoodPlaces(**payload)
            id = foodPlacesCollection.insert_one(food.to_bson()).inserted_id
            return {"message": "create success", "code": 200}
        except Exception as e:
            _throw(e)

    @staticmethod
    def delete_by_id(id):
        try:
            food_place = FoodPlaceService.get_by_id(id)
            FoodPlaceService.assert_food_place(FoodPlaces(**food_place), True)

            foodPlacesCollection.delete_one({"_id": ObjectId(id) })
            return {"message": "delete success", "code": 200}
        except Exception as e:
            _throw(e)

    @staticmethod
    def update(id,payload):
        try:
            if payload['openTimes'] != None : 
                payload['openTimes'] = json.dumps(payload['openTimes'])
        
            food = FoodPlaceService.get_by_id(id)
            food = FoodPlaces( **{**food,**payload})
            FoodPlaceService.assert_food_place(food, True)
            foodPlacesCollection.update_one({"_id": ObjectId(id) }, {"$set":  food.to_bson()})
            return food.to_json()
        except Exception as e:
            _throw(e)

    @staticmethod
    def assert_food_place(food:FoodPlaces, check_auth = False):
        if not food : _throw(NotFoundDataException("can't find food place"))

        if type(food) is list:
            if len(food) == 0: _throw(NotFoundDataException("can't find food place"))
            
        if check_auth is True:
            user: Users = get_current_user()
            if food.userID != user.id: _throw(NotPermissionException("Not permission"))




    
