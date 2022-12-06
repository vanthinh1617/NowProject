"""https://www.youtube.com/watch?v=bM50i7sKwwM"""
import requests
import json 


url = "https://gappapi.deliverynow.vn/api/delivery/get_infos"

post_content = {
    "restaurant_ids": [
                    "277130",

                ]
}

post_header  = {
"x-foody-access-tok en":"",
"x-foody-api-version": "1",
"x-foody-app-type":"1004",
"x-foody-client-id":"",
"x-foody-client-type": "1",
"x-foody-client-version":"3.0.0"

}
if __name__ == '__main__':
    response = requests.post(url,json={"restaurant_ids": [277130]}, headers=post_header)
    print(response.content)