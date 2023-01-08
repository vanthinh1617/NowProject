import requests
import json 
from app.model.db import foodPlacesCollection,foodCategoriesCollection, foodCategoryLangsCollection, foodTypeAndStylesCollection, foodTypeAndStyleLangsCollection, foodLocationsCollection
from app.model.model import FoodPlaces,FoodCategories,FoodImages,FoodOpenTimes,FoodTypeAndStyleLangs, FoodTypeAndStyles, FoodLocations
from app.util.time import stringToDate, timeToSecond
from craw.model.db import nowRawCollection
from bson.objectid import ObjectId
import traceback

class DeliveryService:

    @staticmethod
    def rawToDB(delivery, userID, cloneImages = False):
        foodPlace = {
            "userID" : ObjectId(userID),
            "oldRestaurentID" : delivery['id'],
            "name" : delivery['name'],
            "phone" : delivery['phones'][0],
            # "email" : delivery['email'],
            "website" : delivery['url'],
            "images" : json.dumps(delivery['photos']),
            "openTimes": None,
        }
        if delivery['operating'] is not None and delivery['operating']['status'] == 1: 
            openTime = stringToDate(delivery['operating']['open_time'])
            closeTime = stringToDate(delivery['operating']['close_time'])
            openTimes = {
                    "MONDAY": [
                        {
                            "OPEN": timeToSecond(openTime),
                            "CLOSE": timeToSecond(closeTime)
                        } 
                    ],
                    "TUESDAY": [
                        {
                            "OPEN": timeToSecond(openTime),
                            "CLOSE": timeToSecond(closeTime)
                        } 
                    ],
                    "WEDNESDAY": [
                        {
                            "OPEN": timeToSecond(openTime),
                            "CLOSE": timeToSecond(closeTime)
                        } 
                    ],
                    "THURSDAY": [
                        {
                            "OPEN": timeToSecond(openTime),
                            "CLOSE": timeToSecond(closeTime)
                        } 
                    ],
                    "FRIDAY": [
                        {
                            "OPEN": timeToSecond(openTime),
                            "CLOSE": timeToSecond(closeTime)
                        } 
                    ],
                    "SATURDAY": [
                        {
                            "OPEN": timeToSecond(openTime),
                            "CLOSE": timeToSecond(closeTime)
                        } 
                    ],
                    "SUNDAY": [
                        {
                            "OPEN": timeToSecond(openTime),
                            "CLOSE": timeToSecond(closeTime)
                        } 
                    ]
                }
            foodPlace['openTimes'] = json.dumps(openTimes)
            
        foodPlace = FoodPlaces(**foodPlace)
        id = foodPlacesCollection.insert_one(foodPlace.to_json()).inserted_id

        for category in delivery['categories']:
            id = foodCategoriesCollection.insert_one({
                "foodPlaceID": id
            }).inserted_id

            foodCategoryLangsCollection.insert_one({
                "foodCategoryID": id,
                "lang": "vi",
                "categoryName": category
            })

        if delivery['location_url'] is not None: 
            foodLocationsCollection.insert_one({
                "foodPlaceID": id,
                "address": delivery['address'],
                "city": delivery["location_url"],
                "country": "Việt Nam"
            })

        if  cloneImages is True:
            if delivery['photos'] is not None:
                for photo in delivery['photos']:
                    response = requests.get(photo['value'])
                    width = photo['width']
                    height = photo['height']
                    pathUrl = f"app/static/photos/s{width}x{height}/{photo['value'].split('/')[-1]}"
                    import os
                    os.makedirs(os.path.dirname(pathUrl), exist_ok=True)
                    with open(pathUrl, "wb+") as f: 
                        f.write(response.content)
