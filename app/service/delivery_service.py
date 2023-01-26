
from app.util.time import time_to_second
from app.model.db import foodPlacesCollection
from bson import ObjectId
import datetime

class DeliveryService:
    
    @staticmethod
    def search_global(payload):
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
            total_second = time_to_second(datetime.datetime.now())
            pipelines.append({
                "$match": {
                    "$and" : [
                        { "openTimes.MONDAY": {"$exists": True }},
                        { "openTimes.MONDAY.OPEN": {"$lte": total_second }},
                        { "openTimes.MONDAY.CLOSE": {"$gte": total_second }}
                    ]
                }
            })
        
        pipelines.append( { "$project": {"_id": 1}})
     
        food_places = foodPlacesCollection.aggregate(
            pipeline= pipelines
        )
        listIds = [ foodPlace["_id"]  for foodPlace in  list(food_places) ]
        
        return  {"ids": listIds}
        
        