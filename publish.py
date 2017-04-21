

import SensorData
import random
import time
import json
from pymongo import MongoClient
from pubnub.pubnub import PubNub, SubscribeListener
from pubnub.pnconfiguration import PNConfiguration
from pubnub.exceptions import PubNubException

# Pubnub init
pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-f271816a-f3c4-11e6-88c3-0619f8945a4f'
pnconfig.publish_key = 'pub-c-b4be713a-be4f-4872-b5c8-6232f76df1d4'
pnconfig.ssl = False
pb = PubNub(pnconfig)
channel = 'RMBX'


def writeDB(data, server, port):
    client = MongoClient(server, port)
    db = client.home1

    # writing new data in db
    db.home1.insert_one(data)
    data.pop('_id',None)
    my_listener = SubscribeListener()
    pb.add_listener(my_listener)
    pb.subscribe().channels(channel).execute()
    my_listener.wait_for_connect()
    print 'connected'
    print data
    print type(data)

    while True:
        try:
            envelope = pb.publish().channel(channel).message(data).sync()
            print("publish timetoken: %d" % envelope.result.timetoken)
        except PubNubException as e:
            print 'exception...'
            pass
        # pb.publish().channel(channel).message(data)
        print 'published'
        result = my_listener.wait_for_message_on(channel)
        print 'result message'
        print result.message
        print 'waiting'
        t_sleep = random.randint(0,6)
        print 'T_SLEEP', t_sleep
        time.sleep(t_sleep)



if __name__ == '__main__':
    writeDB(SensorData.sensorData(), 'localhost', 27017)
