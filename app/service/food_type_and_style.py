from app.model.db import foodTypeAndStyleLangsCollection, foodTypeAndStylesCollection
from app.model.model import FoodTypeAndStyles, FoodTypeAndStyleLangs
from app.util.helpers import _throw
from bson import ObjectId

class FoodTypeAndStyleService:
    
    @staticmethod
    def create(payload):
        try:
            foodType = FoodTypeAndStyles(**payload)
            foodTypeAndStylesCollection.insert_one(foodType.to_json())
            return True
        except Exception as e:
            _throw(e)
    
    @staticmethod 
    def update(payload):
        foodType = foodTypeAndStylesCollection.find_one(ObjectId(payload['id']))
        foodType = FoodTypeAndStyles(foodType)
        if foodType is not None: 
            foodType = FoodTypeAndStyles( {**foodType.to_bson(), **payload})
            foodTypeAndStylesCollection.update_one({"_id": ObjectId(payload['id'])}, {
                "$set": foodType.to_bson()
            })
            return True
        else: return False