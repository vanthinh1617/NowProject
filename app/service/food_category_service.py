from app.model.model import FoodCategories, FoodCategoriesLangs, Users, FoodPlaces
from app.model.db import foodCategoryLangsCollection,foodCategoriesCollection
from .food_service import FoodPlaceService
from bson.objectid import ObjectId
from app.util.helpers import _throw
from app.util.exception import NotFoundDataException
class FoodCategoryService: 

    @staticmethod
    def create(payload):
        for lang in payload['categoryLangs']:
            foodCategoryID = foodCategoriesCollection.insert_one({
                "foodPlaceID":  ObjectId(payload['foodPlaceID'])
            }).inserted_id

            if "vn" in lang is not None and lang['vn'] != ""  : 
                FoodCategoryService.save_to_db(lang['vn'], foodCategoryID, 'vn')
                
            if "en" in lang is not None and lang['en'] != "": 
                FoodCategoryService.save_to_db(lang['en'], foodCategoryID, 'en')
                
            # cteLang = FoodCategoriesLangs(**lang)
        return {"message": "save category success!"}
     
    @staticmethod
    def save_to_db(name, foodCategoryID,lang = "vn"):
        foodCategoryLangsCollection.insert_one({
            "categoryName": name,
            "foodCategoryID": ObjectId(foodCategoryID),
            "lang": lang
        })
            
    @staticmethod
    def update(payload):
        category = FoodCategoryService.get_by_id(ObjectId(payload['foodCategoryID']))
        category:FoodCategories = FoodCategories(**category)
        #FoodCategoryService.assertCategory(category=category)
        if payload['categoryLangs']['vn'] != '' and payload['categoryLangs']['vn']  is not  None:
            foodCategoryLangsCollection.update_one({
                "lang": "vn",
                "foodCategoryID": ObjectId(category.id)
            },{
                "$set": {
                    "categoryName": payload['categoryLangs']['vn']
                }
            })
        elif payload['categoryLangs']['en'] != '' and payload['categoryLangs']['en']  is not None:
            foodCategoryLangsCollection.update_one({
                "lang": "en",
                "foodCategoryID": ObjectId(category.id)
            },{
                "$set": {
                    "categoryName": payload['categoryLangs']['en']
                }
            })
        return True

    
    @staticmethod
    def get_by_id(id):
        return foodCategoriesCollection.find_one(id)

    @staticmethod
    def assert_category(category: FoodCategories):
        if not category : _throw(NotFoundDataException("can't find category"))

        foodPlace = FoodPlaceService.get_by_id(category.foodPlaceID)
        FoodPlaceService.assertFoodPlace(FoodPlaces(**foodPlace))

    @staticmethod
    def delete_by_id(id):
        category = FoodCategoryService.get_by_id(id)
        FoodCategoryService.assertCategory(category= category)

        return foodCategoriesCollection.delete_one(id)