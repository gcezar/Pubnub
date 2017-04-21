import json
import threading
import pymongo

'''
Client Listener Thread
'''
class ClientListenerThread(threading.Thread):

	def __init__(self,server,port,queueRef,pnb):
		threading.Thread.__init__(self)
		self.mongoconn = pymongo.MongoClient(server,port)
		self.db = self.mongoconn.stockdb
		self.coll = self.db.stockcollection

		self.clientQueue = queueRef
		self.pnb = pnb

	def run(self):

		try :
			while True :
				print "Before queue block"
				data = self.clientQueue.get()
				print "After queue block"
				print data

				req = json.loads(data)


				self.publishPriceHistory(req['name'],req['backtime'],req['channel'])

		except Exception as e:
			print "Failure in Client Request Handling"
			print e

	def publishPriceHistory(self,idxname,time,channel):

		broadcastDict = []

		timefrom = self.getLastUpdateTime(idxname)

		timefrom = timefrom - (time * 60)

		it = self.coll.find({'name': idxname , 'time' : { '$gte' : timefrom } })

		for item in it:

			broadcastDict.append({ "name"   : item['name'],
						      "value"  : item['value'],
						      "change" : item['change'],
						      "time"   : item['time']
						})

		broadcastData = json.dumps(broadcastDict)
		print 'Broadcasting Price History : ' + broadcastData
		self.pnb.publish(channel,broadcastData)


	def getLastUpdateTime(self,idxname):

		query = [{'$group': {'_id': '$name', 'maxValue': {'$max': '$time'}}}]

		result = self.coll.aggregate(query)

		for entry in result['result']:
			if (entry['_id'] == idxname):
				return entry['maxValue']

		return None
