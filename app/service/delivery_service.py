
from app.util.time import timeToSecond
from app.model.db import foodPlacesCollection
from bson import ObjectId
import datetime

class DeliveryService:
    
    @staticmethod
    def searchGlobal(payload):
        pipelines = [
            
        ]
        payload["isOpen"] = payload["isOpen"]  if payload["isOpen"] is True else False
        if payload['combineCategories'] is not None: 
            pipelines.append({
                "$lookup": {
                    "from": "foodCategories",
                    "localField": "_id",
                    "foreignField": "foodPlaceID",                    
                    "as": "category"
                }
            })
            pipelines.append({
                "$match": {
                    "$and": [
                        {"category.0": { "$exists": True}},
                        {"category._id": {"$in":  payload['combineCategories']} }
                    ]
                }
            })
        if payload["isOpen"] is True:
            totalSecond = timeToSecond(datetime.datetime.now())
            pipelines.append({
                "$match": {
                    "$and" : [
                        { "openTimes.MONDAY": {"$exists": True }},
                        { "openTimes.MONDAY.OPEN": {"$lte": totalSecond }},
                        { "openTimes.MONDAY.CLOSE": {"$gte": totalSecond }}
                    ]
                }
            })
        
        pipelines.append( { "$project": {"_id": 1}})
     
        foodPlaces = foodPlacesCollection.aggregate(
            pipeline= pipelines
        )
        listIds = [ foodPlace["_id"]  for foodPlace in  list(foodPlaces) ]
        
        return  {"ids": listIds}
        
        