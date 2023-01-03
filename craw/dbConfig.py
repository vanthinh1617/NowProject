from pymongo import MongoClient
import traceback
dbList = {
    "PRODUCT": "Now",
    "TEST": "Test"
}

def setClient(name):
    try:
        client = MongoClient('mongodb://localhost:27017/')
        return client[dbList[name]]
    except Exception as e: 
        traceback.print_exc()
        print(e)

def getClient():
    try:
        # for key, val in dbList.items():
        #     print(key)
        # client = setClient(input("Nhập Môi trường: "))
        client = setClient("PRODUCT")

        return client
    except Exception as e: 
        traceback.print_exc()
        print(e)

