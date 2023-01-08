import json, requests, traceback
from craw.util.const import HEADER
class RequestService:
    @staticmethod
    def getRestaurantInfos(restaurantIds):
        url = "https://gappapi.deliverynow.vn/api/delivery/get_infos"
        data = json.dumps({ "restaurant_ids": restaurantIds})
        
        response = requests.post(url= url, data= data, headers= HEADER.POST_HEADER)
        return response.content.decode('utf-8')

    @staticmethod     
    def getIds(cityID):
        try:
            url = "https://gappapi.deliverynow.vn/api/promotion/get_ids"
            response = requests.post(url, headers= HEADER.POST_HEADER, data= json.dumps(
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

    @staticmethod
    def getDetail(id = None):
        deliveryID = id
        if id is None:
            deliveryID = input("mời nhập dilvery id: ")

        idType = 2 
        url = f"https://gappapi.deliverynow.vn/api/delivery/get_detail?id_type={idType}&request_id={deliveryID}"
        response = requests.get(url= url, headers= HEADER.POST_HEADER)
       
        return response.content.decode('utf-8')
    
    @staticmethod
    def searchGlobal(cityID):
        url = "https://gappapi.deliverynow.vn/api/delivery/search_global"
        post_content = {
            "category_group": 1,
            "city_id": cityID,
            "delivery_only": True,
            "keyword": "",
            "sort_type": 8,
            "foody_services": [
                1
            ],
            "full_restaurant_ids": True
        }
        response = requests.post(url,data= json.dumps(post_content), headers=HEADER.POST_HEADER)
        return response.content.decode('utf-8')
    
    @staticmethod
    def getMetadata():
        url = "https://gappapi.deliverynow.vn/api/meta/get_metadata"
        response = requests.get(url, headers=HEADER.POST_HEADER)
        
        return response.content.decode('utf-8')