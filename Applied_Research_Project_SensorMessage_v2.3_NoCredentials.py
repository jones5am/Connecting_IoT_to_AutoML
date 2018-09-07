from time import sleep
from random import uniform
import boto3
         
import RPi.GPIO as GPIO
import time
import PCF8591 as ADC
import math

DO = 17
GPIO.setmode(GPIO.BCM)

  
#### Programatically connecting to my Dynamo DB Table
client = boto3.resource('dynamodb', region_name = 'us-east-1', aws_access_key_id = '#####',aws_secret_access_key = '#####')
table = client.Table('Applied_Research')



#### Thermistor Code ####

def setup():
	ADC.setup(0x48)
	GPIO.setup(DO, GPIO.IN)



def loop():
	ID = 0
	while True:
		analogVal = ADC.read(0)
		Vr = 5 * float(analogVal) / 255
		Rt = 10000 * Vr / (5 - Vr)
		temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
		temp = temp - 273.15
		print ('temperature = ', temp, 'Celsius')
		
		ID += 1
		localtime = time.asctime(time.localtime(time.time()))  
		table.put_item(Item = {'ID':ID,'Temp':str(temp),'Timestamp':localtime}) #where the record is actually inserted (in celsius). The ID field is the primary key and the only required field

		time.sleep(10)

		

if __name__ == '__main__':
	try:
		setup()
		loop()
	except KeyboardInterrupt: 
		pass	

    

