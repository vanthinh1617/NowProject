"""https://www.youtube.com/watch?v=bM50i7sKwwM"""
import requests
import json 
from app.model.db import foodPlacesCollection,foodCategoriesCollection, foodTypeAndStylesCollection, foodTypeAndStyleLangsCollection
from app.model.model import FoodPlaces,FoodCategories,FoodImages,FoodOpenTimes,FoodTypeAndStyleLangs, FoodTypeAndStyles
from bson.objectid import ObjectId
from pymongo import MongoClient
from craw.dbConfig import getclient
from craw.util.helper import splitUrl
import traceback


client = getclient()

post_header  = {
"x-foody-access-token":"",
"x-foody-api-version": "1",
"x-foody-app-type":"1004",
"x-foody-client-id":"",
"x-foody-client-type": "1",
"x-foody-client-language": "vi",
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

   
def getMetadata():
    url = "https://gappapi.deliverynow.vn/api/meta/get_metadata"
    response = requests.get(url, headers=post_header)
    
    return response.content.decode('utf-8')

def importData():
    print("1: lưu vào file")
    print("2: lưu vào database: ")
    manager = input("Nhập lựa chọn: ")
    if manager == 1:
        userID = input("Nhập userID:  ")
        with open('delivery_info.json', "r", encoding="utf-8") as f:
            delivery_info_json = json.load(f)
            items = []

            for place in delivery_info_json['delivery_infos']:
                foodPlace = {
                                "name": place['name'], 
                                "phone": place['phones'][0],
                                "userID": ObjectId(userID),
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

def getCategories():
    metadata = json.loads( getMetadata() )
    categories = metadata['reply']['country']['now_services'][0]["categories"]
    try: 
        for category in categories:
            foodStyle = FoodTypeAndStyles()
            # foodStyleLangs = FoodTypeAndStyleLangs()
            foodStyle.type = category['code']
            foodStyleID = foodTypeAndStylesCollection.insert_one(foodStyle.to_json()).inserted_id
            # foodStyleLangs.foodTyleAndStyleID = foodStyleID
            # foodStyleLangs.lang = "vn"


            # for x, i  in category.items():
            #     print(i)
            #     break
    except Exception as e:
        print(e)
    


def schedule(num):
    match num: 
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass
        case 4:
            getCategories()
        case _:
            pass
   

def main():
    while(True): 
        print("==============")
        print("1: search_global")
        print("2: get info")
        print("3: importData")
        print("4: clone categories")
        print("0: thoát ra")
        print("==============")
        num  = int(input("Mời nhập lựa chọn:  "))
        schedule(num= num)
        if num == 0 : break

if __name__ == '__main__':
    # search_global()
    # getInfo()
    #importData()
    try:
        main()
    except Exception as e:
        print (e)
        print("\==============")
        print("lựa chọn không hợp lệ")
        print("\==============\n")
        main()



