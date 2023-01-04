"""https://www.youtube.com/watch?v=bM50i7sKwwM"""
import requests
import json 
from app.model.db import foodPlacesCollection,foodCategoriesCollection, foodCategoryLangsCollection, foodTypeAndStylesCollection, foodTypeAndStyleLangsCollection, foodLocationsCollection
from app.model.model import FoodPlaces,FoodCategories,FoodImages,FoodOpenTimes,FoodTypeAndStyleLangs, FoodTypeAndStyles, FoodLocations
from app.service.user_service import UserService
from app.util.time import stringToDate, timeToSecond
from craw.model.db import client
from craw.util.helper import splitUrl, chunks
from craw.model.db import dropCollection
from craw.model.db import nowRawCollection
import traceback

userSession = None 
metadata =  None
cityID = 217
post_header  = {
    "x-foody-access-token":"",
    "x-foody-api-version": "1",
    "x-foody-app-type":"1004",
    "x-foody-client-id":"",
    "x-foody-client-type": "1",
    "x-foody-client-language": "vi",
    "x-foody-client-version":"3.0.0"
}

def getDetail(id = None):
    deliveryID = id
    if id is None:
        deliveryID = input("mời nhập dilvery id: ")

    idType = 2 
    url = f"https://gappapi.deliverynow.vn/api/delivery/get_detail?id_type={idType}&request_id={deliveryID}"
    response = requests.get(url= url, headers= post_header)
    content = json.loads( response.content.decode('utf-8'))
   
    return response.content.decode('utf-8')
    

def getRestaurantInfos(restaurantIds):
    url = "https://gappapi.deliverynow.vn/api/delivery/get_infos"
    data = json.dumps({ "restaurant_ids": restaurantIds})
    
    response = requests.post(url= url, data= data, headers= post_header)
    return response.content.decode('utf-8')

def searchGlobal():
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
    return response.content.decode('utf-8')




   
def getMetadata():
    url = "https://gappapi.deliverynow.vn/api/meta/get_metadata"
    response = requests.get(url, headers=post_header)
    
    return response.content.decode('utf-8')

def cloneData():
    try:
        response = json.loads(searchGlobal())
        results = response['reply']['search_result'][0]['restaurant_ids']
        nowRawCollection = client['nowRaw']
        chunkedArray = list(chunks(results, 25))
        
        for ids in chunkedArray:
            json.dumps({ "restaurant_ids": list(ids)})
            response = json.loads(getRestaurantInfos(ids))
            nowRawCollection.insert_many(response['reply']['delivery_infos'])

        return True
    except Exception as e:
        traceback.print_exc()
        print(e)


def getIds():
    try:
        url = "https://gappapi.deliverynow.vn/api/promotion/get_ids"
        response = requests.post(url, headers= post_header, data= json.dumps(
            {
                "city_id": cityID,
                "foody_service_id": 1,
                "sort_type": 0,
                "promotion_status": 1
            }
        ))
        return response.content.decode('utf-8')
        # return 
    
    except Exception as e:
        traceback.print_exc()
        print(e)
       
def setCity():
    try:
        metadata = json.loads(getMetadata())
        for city in metadata['reply']['country']['cities']:
            print(f"Thành phố: {city['name']}  code: {city['id']}" )
        cityID = int(input("Chọn thành phố: "))
    except Exception as e:
        traceback.print_exc()
  


def importRawToDB():
    results = list(nowRawCollection.find({}))

    for delivery in results:
        foodPlace = {
            "userID" : userSession.id,
            "oldRestaurentID" : delivery['id'],
            "name" : delivery['name'],
            "phone" : delivery['phones'][0],
            # "email" : delivery['email'],
            "website" : delivery['url'],
            "images" : json.dumps(delivery['photos']),
            "openTimes": None,
        }
        if delivery['operating'] is not None: 
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
                    
def schedule(num):
    match num: 
        case 1:
            cloneData()
            pass
        case 2:
            importRawToDB()
            pass
        case 3:
            getDetail()
            pass
        case 4:
            pass
        case 5:
            dropCollection()
        case _:
            pass
   
if metadata is None:
    metadata = getMetadata()

def main():
    while(True): 
        print("==============")
        print("1: clone data")
        print("2: importData")
        print("5: xoá toàn bộ collection")
        print("0: thoát ra")
        print("==============")
        num  = int(input("Mời nhập lựa chọn:  "))
        schedule(num= num)
        if num == 0 : break

if __name__ == '__main__':
    try:
        if userSession is None: 
            userSession = UserService.get_by_user_name(input("Nhập username:  "))
            if userSession is None:
                raise Exception("Cant find user ")
        setCity()
        main()
    except Exception as e:
        traceback.print_exc()
        print (e)
        print("\==============")
        print("lựa chọn không hợp lệ")
        print("\==============\n")
        main()



