from MCP3008 import MCP3008
import http.client
import urllib
import time
import Adafruit_DHT
pin = 4 #DHT11 input
sensor = Adafruit_DHT.DHT11
key = 'H06YCX0KHDSHJD2O'
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
PIR_input = 16 #read PIR Output
Relay_input = 19
Buzzer_input = 6
GPIO.setup(PIR_input, GPIO.IN)
GPIO.setup(Relay_input, GPIO.OUT)
GPIO.setup(Buzzer_input, GPIO.OUT)
lcd_rs=18
lcd_en=23
lcd_d4=24
lcd_d5=25
lcd_d6=12
lcd_d7=20
lcd_coloumns=16
lcd_rows=2
lcd=LCD.Adafruit_CharLCD(lcd_rs,lcd_en,lcd_d4,lcd_d5,lcd_d6,lcd_d7,lcd_coloumns,lcd_rows)

def thermometer():
    while True:
        if(GPIO.input(PIR_input)):
            print("Motion detected")
        else:
            print("Motion not detected")
            time.sleep(1)
        adc=MCP3008()
        value=adc.read(channel=0)
        if(value > 100):
            GPIO.output(Relay_input, 0)
            GPIO.output(Buzzer_input,1)
        else:
            GPIO.output(Relay_input, 1)
            GPIO.output(Buzzer_input,0)
        print("Air Quality Index = ",value)
        lcd.message("AQI = ")
        lcd.set_cursor(0,1)
        lcd.message(str(round(value)))
        lcd.set_cursor(9,0)
        time.sleep(3)
        lcd.clear()
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        print(humidity, temperature)
        lcd.message("humidity")
        lcd.set_cursor(0,1)
        lcd.message(str(round(humidity)))
        lcd.set_cursor(9,0)
        time.sleep(3)
        lcd.clear()
        lcd.message("temperature")
        lcd.set_cursor(0,1)
        lcd.message(str(round(temperature)))
        lcd.set_cursor(9,0)
        time.sleep(3)
        lcd.clear()
        params = urllib.parse.urlencode({'field1': temperature, 'field2': humidity, 'key':key })
        headers = {"Content-typZZe": "application/x-www-form- urlencoded","Accept": "text/plain"}
        conn = http.client.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print (response.status, response.reason)
            data = response.read()
            conn.close()
        except:
            print("connection failed")
            break
    while True:
        thermometer()
        lcd.clear()
        time.sleep(2)
