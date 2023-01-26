import datetime

def time_to_second(time_now):
    time_now = time_now.strftime("%H:%M:%S")
    hour, minus, second = time_now.split(":")
    hour =  int(hour) * 3600
    minus = int(minus) * 60
    second = int(second)
    
    return  hour + minus + second

def string_to_date(str):
    time = datetime.datetime.strptime(str, '%H:%M:%S').time()
    return time