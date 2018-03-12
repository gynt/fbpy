import datetime
starttime=datetime.datetime.strptime("2017-09-01","%Y-%m-%d").timestamp()
#01-09-2017: 1504216800

def time_to_datetime(year, month, day, hours=0, months=0, seconds=0):
    return datetime_to_epoch(datetime.datetime.strptime(str(year)+str(month)+str(day)+str(hours)+str(months)+str(seconds),"%Y%m%d"))

def day_to_epoch(year, month, day):
    return datetime_to_epoch(datetime.datetime.strptime(str(year)+str(month)+str(day),"%Y%m%d"))

def parse_created_time(created_string):
    return datetime.datetime.strptime(created_string, "%Y-%m-%dT%H:%M:%S+0000")

def datetime_to_epoch(t):
    return int(t.timestamp())
