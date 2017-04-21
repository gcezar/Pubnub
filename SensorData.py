import random
import numpy as np

def sensorData():
    x = np.linspace(-np.pi, np.pi, 201)
    offset = round(random.uniform(-5.0,5.0),2)
    # do data processing
    current = max(np.sin(x)+offset)*0.7071
    volt = 127.
    power = str(volt*current)
    # get location of device
    location = 'CB1'
    # get time
    time = '124334'
    # json format
    data = {'data':power,'location':location,'time':time}
    return data

if __name__ == '__main__':
    a = sensorData()
    print a
