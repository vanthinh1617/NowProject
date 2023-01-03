"""https://www.youtube.com/watch?v=bM50i7sKwwM"""
import requests
import json 
from app.model.db import dropCollection
from app.model.db import foodPlacesCollection,foodCategoriesCollection, foodTypeAndStylesCollection, foodTypeAndStyleLangsCollection
from app.model.model import FoodPlaces,FoodCategories,FoodImages,FoodOpenTimes,FoodTypeAndStyleLangs, FoodTypeAndStyles
from bson.objectid import ObjectId
from pymongo import MongoClient
from craw.dbConfig import getClient
from craw.util.helper import splitUrl, chunks
import traceback


metadata =  None
client = None
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
  

def schedule(num):
    match num: 
        case 1:
            cloneData()
            pass
        case 2:
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
        print("5: xoá toàn bộ collection")
        print("0: thoát ra")
        print("==============")
        num  = int(input("Mời nhập lựa chọn:  "))
        schedule(num= num)
        if num == 0 : break

if __name__ == '__main__':
    try:
        client = getClient()
        setCity()
        main()
    except Exception as e:
        print (e)
        print("\==============")
        print("lựa chọn không hợp lệ")
        print("\==============\n")
        main()



