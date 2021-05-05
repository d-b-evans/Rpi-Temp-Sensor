#source https://roboticadiy.com/raspberry-pi-4-data-logger-dht11-dht22-sensor-data-logger/
#Accessed 5/4/2021 running in Python 2.7.16

#note for myself: if writing to CSV to you need to 'import csv'?
#another note: can the 'dht11' or 'dht22' library be used instead of Adafruit_DHT (which is deprecated)

import Adafruit_DHT
import time

sensor = Adafruit_DHT.DHT11

#DHT pin connects to GPIO number on next line(s)
sensor1 = 2
sensor2 = 14

#create a variable to control the while loop
running = True #silly extra variable but I'm ok with it

#new .txt file created with header 
#the 'a' argument below stands for append
#you can pass it a 'w' arg for write (but that overwrites the original file)
#there's some other args too
file = open('sensor_readings.txt', 'a')
file.write('time and date, temp1 (C), temp1 (F), humidity1, temp2 (C), temp2 (F) humidity2\n')

#loop forever
while running:

    try:
        #read the humidity and temperature
        humidity1, temperature1 = Adafruit_DHT.read_retry(sensor, sensor1)
        humidity2, temperature2 = Adafruit_DHT.read_retry(sensor, sensor2)

        #uncomment the line below to convert to Fahrenheit
        temperature1_f = temperature1 * 9/5.0 + 32
        temperature2_f = temperature2 * 9/5.0 + 32


        #sometimes you won't get a reading and
        #the results will be null
        #the next statement guarantees that
        #it only saves valid readings
        if humidity1 is not None and temperature1 is not None: #ONLY CHECKS ONE OF THE SENSORS. BAD CODE. BEING LAZY

            #print temperature and humidity1
            print('Temperature1 = ' + str(temperature1) +','+ 'Temperature1 Fahrenheit = ' + str(temperature1_f) +',' + 'Humidity1 = ' + str(humidity1))
            print('Temperature2 = ' + str(temperature2) +','+ 'Temperature2 Fahrenheit = ' + str(temperature2_f) +',' + 'Humidity2 = ' + str(humidity2))

            #save time, date, temperature in Celsius, temperature in Fahrenheit and humidity in .txt file
            file.write(time.strftime('%H:%M:%S %d/%m/%Y') + ', ' + str(temperature1) + ', '+ str(temperature1_f)+', ' + str(humidity1) + ', ' + str(temperature2) + ', '+ str(temperature2_f)+', ' + str(humidity2) + '\n')
            time.sleep(5)

        else:
            print('Failed to get reading. Try again!')
            time.sleep(1)

    except KeyboardInterrupt:
        print ('Program stopped')
        running = False
        file.close()