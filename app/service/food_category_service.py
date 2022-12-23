from app.model.model import FoodCategories, FoodCategoriesLangs, Users, FoodPlaces
from app.model.db import foodCategoryLangsCollection,foodCategoriesCollection
from .food_service import FoodPlaceService
from bson.objectid import ObjectId
class FoodCategoryService: 

    @staticmethod
    def create(payload):
        for lang in payload['categoryLangs']:
            foodCategoryID = foodCategoriesCollection.insert_one({
                "foodPlaceID":  ObjectId(payload['foodPlaceID'])
            }).inserted_id

            if lang['vn'] != "" and lang['vn'] is not None: 
                FoodCategoryService.saveToDB(lang['vn'], foodCategoryID, 'vn')
                
            if lang['en'] != "" and lang['en'] is not None: 
                FoodCategoryService.saveToDB(lang['en'], foodCategoryID, 'en')
                
            # cteLang = FoodCategoriesLangs(**lang)
        return True
     
    @staticmethod
    def saveToDB(name, foodCategoryID,lang = "vn"):
        foodCategoryLangsCollection.insert_one({
            "categoryName": name,
            "foodCategoryID": ObjectId(foodCategoryID),
            "lang": lang
        })
            
    @staticmethod
    def update(payload):
        category = FoodCategoryService.getByID(ObjectId(payload['foodCategoryID']))
        category:FoodCategories = FoodCategories(**category)
        FoodCategoryService.assertCategory(category=category)
        if payload['categoryLangs']['vn'] != '' and payload['categoryLangs']['vn']  is None:
            foodCategoryLangsCollection.update_one({
                "lang": "vn",
                "foodCategoryID": ObjectId(category.id)
            },{
                "$set": {
                    "categoryName": payload['categoryLangs']['vn']
                }
            })
        elif payload['categoryLangs']['en'] != '' and payload['categoryLangs']['en']  is None:
            foodCategoryLangsCollection.update_one({
                "lang": "en",
                "foodCategoryID": ObjectId(category.id)
            },{
                "$set": {
                    "categoryName": payload['categoryLangs']['en']
                }
            })

    
    @staticmethod
    def getByID(id):
        return foodCategoriesCollection.find_one(id)

    @staticmethod
    def assertCategory(category: FoodCategories):
        foodPlace = FoodPlaceService.getByID(category.foodPlaceID)
        FoodPlaceService.assertFoodPlace(FoodPlaces(**foodPlace))
