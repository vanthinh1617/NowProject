from app.model.db import foodPlacesCollection, foodCategoryLangsCollection, foodCategoriesCollection
from app.model.model import FoodPlaces, Users, FoodCategories, FoodCategoriesLangs
from bson.objectid import ObjectId
from app.util.helpers import _throw
from app.util.jwt import get_current_user
from app.util.exception import NotPermissionException, NotFoundDataException
from flask import request
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
                "from": "foodImages",
                "let": {"placeID": "$_id"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$eq": ["$foodPlaceID", "$$placeID"] 
                            }
                        }
                    },
                    {"$project": { "_id": 0, "value": {"$arrayElemAt": ["$images", 0] }}},
                ],
                "as": "images"
            }},
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
                            {"$project": {"_id": 0, "categoryName": 1}}
                        ],
                        "as": "langs"
                    }}
                ],
                "as": "categories"
            }}           
        ])

        return list(result)

    @staticmethod
    def create(payload):
        try:
            lang = request.cookies.get('lang')
            user: Users = get_current_user()
            food = FoodPlaces(**payload)
            id = foodPlacesCollection.insert_one(food.to_bson()).inserted_id
            if payload['categories'] and id is None:
                for category in payload['categories']: 
                    FoodCategoryService.save(category, lang, id)

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
            food = FoodPlaceService.getByID(id)  
            food = FoodPlaces( **{**food,**payload})
            FoodPlaceService.assertFoodPlace(food)
            foodPlacesCollection.update_one({"_id": ObjectId(id) }, {"$set":  food.to_bson()})
            return food.to_json()
        except Exception as e:
            _throw(e)

    @staticmethod
    def assertFoodPlace(food:FoodPlaces):
        user: Users = get_current_user()
        if not food : _throw(NotFoundDataException("can't find food place"))
        if user is not None:
            if food.userID != user.id: _throw(NotPermissionException("Not permission"))



class FoodCategoryService:

    # def getList(lang: str = 'vn'):

    #     return foodCategoryLangsCollection.aggregate()
    @staticmethod
    def save(lang: str ="vn", name: str = "", foodPLaceID: int = 0):
        if name is None or foodPLaceID == 0:
            _throw('parameter isvalid')

        foodPlace =  foodPlacesCollection.find_one({"_id": ObjectId(foodPLaceID)})

        FoodPlaceService.assertFoodPlace(foodPLaceID)
        
        foodCategory = foodCategoriesCollection.insert_one({
            "foodPlaceID": foodPLaceID
        })
        
        foodCateLangID =  foodCategoryLangsCollection.insert_one({
            "categoryName": name,
            "lang": lang,
            "foodCategoryID": foodCategory.inserted_id
        }).inserted_id

        if foodCateLangID is None: _throw("can't create category")
        return True

    
