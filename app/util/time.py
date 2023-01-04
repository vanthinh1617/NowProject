import datetime

def timeToSecond(timeNow):
    timeNow = timeNow.strftime("%H:%M:%S")
    hour, minus, second = timeNow.split(":")
    hour =  int(hour) * 3600
    minus = int(minus) * 60
    second = int(second)
    
    return  hour + minus + second

def stringToDate(str):
    time = datetime.datetime.strptime(str, '%H:%M:%S').time()
    return time