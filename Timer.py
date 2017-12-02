import time

first_time = time.time() * 1000
last_time = first_time

def Timer():
    global last_time
    diff = time.time() * 1000 - last_time
    last_time = time.time()*1000
    return diff

def TotalTime():
    return time.time() * 1000 - first_time
