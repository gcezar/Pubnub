import random
import pymongo

def getUpdatedPrice(coll):

	#Random select the index whose price is to be updated
	idx = random.sample(metadataDescr,1)

	#Randomly get a price increment in range of 1.0 to 10.0
	#It is assumed that price delta will always be in this range
	pricedelta = round(random.uniform(1.0,10.0),2)

	#Randomly get the direction of price change
	#Either positive or negative
	pricedir = random.randint(0,1)

	#Get the current price of index
	currprice = getCurrentPrice(coll,idx[0])

	#Calculate new price of index based on pricedelta and pricedir
	if(pricedir):
		newprice = round(currprice + pricedelta,2)
		pricedeltastr = '+'+str(pricedelta)
	else :
		newprice = round(currprice - pricedelta,2)
		pricedeltastr = '-'+str(pricedelta)

	print "New Price for " + idx[0] + " : " + str(newprice)
	#Get the current time of update
	updateTime = getCurrentTimeInSecs()

	#Return the new index price
	return {
			'name'     : idx[0] ,
			'value'    : newprice ,
			'change'   : pricedeltastr ,
			'time'     : updateTime
		}
