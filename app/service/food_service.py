from app.model.db import foodPlacesCollection
from app.model.model import FoodPlaces, Users
from bson.objectid import ObjectId
from app.util.helpers import _throw
from app.util.jwt import get_current_user
from app.util.exception import NotPermissionException, NotFoundDataException
class FoodPlaceService:
    @staticmethod
    def getList(page= 1, pageSize = 30):
        page = int(page)
        pageSize = int(pageSize)
        listFood =  foodPlacesCollection.find().skip((page -1) * pageSize).limit(pageSize)
        return list(listFood)

    @staticmethod
    def getByID(id):
        food =  foodPlacesCollection.find_one({"_id": ObjectId(id)})
        return food

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


        