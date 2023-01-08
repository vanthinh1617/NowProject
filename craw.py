import json 
from app.model.db import foodPlacesCollection,foodCategoriesCollection, foodCategoryLangsCollection, foodTypeAndStylesCollection, foodTypeAndStyleLangsCollection, foodLocationsCollection
from app.service.user_service import UserService
from craw.model.db import client,  dropCollection, nowRawCollection
from craw.util.helper import  chunks
from craw.service.DeilveryService import DeliveryService
from craw.service.RequestService import RequestService
import traceback
userSession = None 
metadata =  None
cityID = None

def cloneData():
    try:
        response = json.loads(RequestService.searchGlobal(cityID= cityID))
        results = response['reply']['search_result'][0]['restaurant_ids']
        chunkedArray = list(chunks(results, 25))
        
        for ids in chunkedArray:
            response = json.loads(RequestService.getRestaurantInfos(ids))
            nowRawCollection.insert_many(response['reply']['delivery_infos'])

        return True
    except Exception as e:
        traceback.print_exc()
        print(e)


def setCity():
    try:
        metadata = json.loads(RequestService.getMetadata())
        for city in metadata['reply']['country']['cities']:
            print(f"Thành phố: {city['name']}  code: {city['id']}" )
        return int(input("Chọn thành phố: "))
    except Exception as e:
        traceback.print_exc()
  


def importRawToDB(cloneImages = False):
    results = list(nowRawCollection.find({
        "city_id": cityID
    }))

    for delivery in results:
        DeliveryService.rawToDB(delivery= delivery,userID= userSession.id, cloneImages= cloneImages)

                    
def schedule(num):
    match num: 
        case 1:
            cloneData()
            pass
        case 2:
            importRawToDB(cloneImages= False)
            pass
        case 3:
            # setCity()
            pass
        case 4:
            # getDetail()
            pass
        case 5:
            dropCollection()
        case _:
            pass
   
if metadata is None:
    metadata = RequestService.getMetadata()

def main():
    while(True): 
        print("==============")
        print("1: clone data")
        print("2: import data đã clone theo city id")
        print("4: clone theo link detail")
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
        cityID = setCity()
        main()
    except Exception as e:
        traceback.print_exc()
        print (e)
        print("\==============")
        print("lựa chọn không hợp lệ")
        print("\==============\n")
        main()



