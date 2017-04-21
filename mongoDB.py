import pymongo
import random
from pymongo import MongoClient
from pubnub.pubnub import PubNub, SubscribeListener
from pubnub.pnconfiguration import PNConfiguration
from pubnub.enums import PNStatusCategory
import ClientListenerThread
import Queue
import getUpdatedPrice


def startStockPicker(server,port):
    global globalQueueRef

    mongoconn = MongoClient(server, port)
    db = mongoconn.stockdb
    coll = db.stockcollection

    coll.create_index([('time', pymongo.DESCENDING)])

    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = 'sub-c-f271816a-f3c4-11e6-88c3-0619f8945a4f'
    pnconfig.publish_key = 'pub-c-b4be713a-be4f-4872-b5c8-6232f76df1d4'
    pnconfig.ssl = False
    pb = PubNub(pnconfig)

    # metaDataInit(coll)

    updateTime = 10
	numOfItems = 4

    random.seed()

    clientQueue = Queue()
	clientListener = ClientListenerThread(server,port,clientQueue,pb)
	clientListener.start()

    globalQueueRef = clientQueue

    pb.subscribe().channels('stockhistory').execute()

    stock = {'name':'NASDAQ', 'value':4630.60, 'change':'+6.06','time':1}
    coll.insert(stock)
