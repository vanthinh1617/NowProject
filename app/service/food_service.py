from app.model.db import foodPlacesCollection
from app.model.model import FoodPlaces, Users
from bson.objectid import ObjectId
from app.util.helpers import _throw
from app.util.jwt import get_current_user
class FoodPlaceService:
    @staticmethod
    def getList(page= 1, pageSize = 30):
        page = int(page)
        pageSize = int(pageSize)
        listFood =  foodPlacesCollection.find().skip((page -1) * pageSize).limit(pageSize)
        return list(listFood)

    @staticmethod
    def getByID(id):
        return foodPlacesCollection.find_one({"_id": ObjectId(id)})

    @staticmethod
    def create(payload):
        try:
            user: Users = get_current_user()
            food = FoodPlaces(**payload)
            food.userID = user.id
            foodPlacesCollection.insert_one(food.to_bson())
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
            food = FoodPlaceService.isValid(FoodPlaceService.getByID(id) )
            
            food = {**food.to_bson(), **payload}
            print(food)
            return foodPlacesCollection.update_one({"_id": ObjectId(id) }, {"$set":  food})
        except Exception as e:
            _throw(e)

    @staticmethod
    def isValid(food):
        user: Users = get_current_user()
        food = FoodPlaces(**food) 
        assert food , "can't find item"
        assert food.userID == user.id, "Unauthorized"
        
        return food