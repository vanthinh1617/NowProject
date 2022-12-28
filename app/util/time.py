
def timeToSecond(timeNow):
    timeNow = timeNow.strftime("%H-%M")
    hour, minus = timeNow.split("-")
    hour =  int(hour) * 3600
    minus = int(minus) * 60
    
    return  hour + minus
