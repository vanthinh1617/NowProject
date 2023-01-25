from app.model.db import foodPlacesCollection, foodCategoryLangsCollection, foodCategoriesCollection
from app.model.model import FoodPlaces, Users, FoodCategories, FoodCategoriesLangs
from bson.objectid import ObjectId
from app.util.helpers import _throw
from app.util.jwt import get_current_user
from app.util.exception import NotPermissionException, NotFoundDataException
from app.util.file import SaveFileToLocal
from app.service.food_type_and_style import FoodTypeAndStyleService
from flask import request
import json, os
class FoodPlaceService:
    @staticmethod
    def getList(page= 1, pageSize = 30):
        page = int(page)
        pageSize = int(pageSize)
        listFood =  foodPlacesCollection.find().skip((page -1) * pageSize).limit(pageSize)
        return list(listFood)

    @staticmethod
    def getByID(id):
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
        if len(list(result)) ==  0:
           raise Exception("can't find user")

        return list(result)[0] 

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
    def deleteByID(id):
        try:
            foodPlacesCollection.delete_one({"_id": ObjectId(id) })
            return {"message": "delete success", "code": 200}
        except Exception as e:
            _throw(e)

    @staticmethod
    def update(id,payload):
        try:
            if payload['openTimes'] != None : 
                payload['openTimes'] = json.dumps(payload['openTimes'])
                
            if 'files'  in request.files:  
                files = request.files.getlist('files')
                SaveFileToLocal.process(files)
        
            # food = FoodPlaceService.getByID(id)  
            # food = FoodPlaces( **{**food,**payload})
            # FoodPlaceService.assertFoodPlace(food)
            # foodPlacesCollection.update_one({"_id": ObjectId(id) }, {"$set":  food.to_bson()})
            # return food.to_json()
        except Exception as e:
            _throw(e)

    @staticmethod
    def assertFoodPlace(food:FoodPlaces):
        user: Users = get_current_user()
        if not food : _throw(NotFoundDataException("can't find food place"))
        if food.userID != user.id: _throw(NotPermissionException("Not permission"))




    
