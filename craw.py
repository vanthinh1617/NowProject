"""https://www.youtube.com/watch?v=bM50i7sKwwM"""
import requests
import json 
from app.model.db import foodPlacesCollection,foodCategoriesCollection
from app.model.model import FoodPlaces,FoodCategories,FoodImages,FoodOpenTimes
from bson.objectid import ObjectId
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['Test']

post_header  = {
"x-foody-access-token":"",
"x-foody-api-version": "1",
"x-foody-app-type":"1004",
"x-foody-client-id":"",
"x-foody-client-type": "1",
"x-foody-client-version":"3.0.0"
}



def getInfo():
    url = "https://gappapi.deliverynow.vn/api/delivery/get_infos"
    r = open('delivery.json','r')
    json_delivery_info = json.load(r)

    response = requests.post(url,data= json.dumps(json_delivery_info), headers=post_header)
    with open('delivery_info.json', "w", encoding="utf-8") as f:
        f.write(response.content.decode('utf-8'))

def search_global():
    url = "https://gappapi.deliverynow.vn/api/delivery/search_global"
    post_content = {
        "category_group": 1,
        "city_id": 219,
        "delivery_only": True,
        "keyword": "",
        "sort_type": 8,
        "foody_services": [
            1
        ],
        "full_restaurant_ids": True
    }
    response = requests.post(url,data= json.dumps(post_content), headers=post_header)
    f = open('delivery.json','w')
    f.write(response.content.decode('utf-8'))
    f.close()

def splitUrl(url):
    urls = url.split('/')
    return urls[len(urls)-1]

def cloneImages():
    with open('delivery_info.json', "r", encoding="utf-8") as f:
        delivery_info_json = json.load(f)
        for index,place in enumerate(delivery_info_json['delivery_infos']):
            atTheEnd = len(place["photos"]) - 1
            url =   place['photos'][atTheEnd]['value']
            res = requests.get(url)
            url = splitUrl(place['photos'][atTheEnd]['value'])
            with open('app/static/photos/'+url,'wb') as f:
                f.write(res.content)

   

def importData():
     with open('delivery_info.json', "r", encoding="utf-8") as f:
        delivery_info_json = json.load(f)
        items = []

        for place in delivery_info_json['delivery_infos']:
            foodPlace = {
                            "name": place['name'], 
                            "phone": place['phones'][0],
                            "userID": ObjectId("6390066a9e05a5892608c786"),
                            'images': place['photos']
                        }
            temp = FoodPlaces(**foodPlace)
            items.append(temp.to_json())

        foodPlaceIds = db.foodPlaces.insert_many(items).inserted_ids

        for intex,place in enumerate(items):
            place['_id'] =  foodPlaceIds[intex]

        for index,place in enumerate(delivery_info_json['delivery_infos']):
            atTheEnd = len(place["photos"]) - 1
            url =   place['photos'][atTheEnd]['value']
            url = splitUrl(place['photos'][atTheEnd]['value'])
            food= FoodImages()
            food.images = [url]
            food.foodPlaceID = items[index]['_id']
            db.foodImages.insert_one(food.to_bson())

if __name__ == '__main__':
    # search_global()
    # getInfo()
    importData()

