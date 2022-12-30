from pymongo import MongoClient

dbList = {
    "PRODUCT": "Now",
    "TEST": "Test"
}

def setClient(name):
    client = MongoClient('mongodb://localhost:27017/')
    client[dbList[name]]
    return client

def getclient():
    # for key, val in dbList.items():
    #     print(key)

    # client = setClient(input("Nhập Môi trường: "))
    client = setClient("PRODUCT")

    return client