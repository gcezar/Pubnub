## Web-controlled LED

#import RPi.GPIO as GPIO
#import time
#import sys
from pubnub.pubnub import PubNub, SubscribeListener
from pubnub.pnconfiguration import PNConfiguration
from pubnub.enums import PNStatusCategory


#GPIO.setmode (GPIO.BCM)

if __name__ == '__main__':

	LED_PIN = 4

	#GPIO.setup(LED_PIN,GPIO.OUT)

	pnconfig = PNConfiguration()
	pnconfig.subscribe_key = 'sub-c-f271816a-f3c4-11e6-88c3-0619f8945a4f'
	pnconfig.publish_key = 'pub-c-b4be713a-be4f-4872-b5c8-6232f76df1d4'
	pnconfig.ssl = False

	pb = PubNub(pnconfig)
	# pb = PubNub(publish_key='pub-c-b4be713a-be4f-4872-b5c8-6232f76df1d4', subscribe_key='sub-c-f271816a-f3c4-11e6-88c3-0619f8945a4f')

	channel = 'RMBX'
	print 'SUBSCRIBING...'
	my_listener = SubscribeListener()
	pb.add_listener(my_listener)
	pb.subscribe().channels('RMBX').execute()
	my_listener.wait_for_connect()

	result = my_listener.wait_for_message_on('RMBX')
	print(result.message)
	print 'PASSED...'






# pb.subscribe(channels=channel, callback=_callback, error=_error)
