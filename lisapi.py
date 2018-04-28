# -*- coding: utf-8 -*-

import os
import commands
import RPi.GPIO as gpio
from flask import Flask, jsonify

app = Flask(__name__)

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

@app.route('/api/status', methods=['GET'])
def getStatus():

  status = {}

  temp = commands.getoutput("vcgencmd measure_temp | cut -c 6-12")

  quantProc = commands.getoutput("ps -aux | wc -l")

  mem_total = commands.getoutput("free -h | grep 'Mem' | cut -c 16-19")
  mem_used = commands.getoutput("free -h | grep 'Mem' | cut -c 29-31")
  mem_free = commands.getoutput("free -h | grep 'Mem' | cut -c 41-43")

  uptime = commands.getoutput("uptime -p")

  total = commands.getoutput("df -h | grep '/dev'| cut -c 18-20 | head -1")
  used = commands.getoutput("df -h | grep '/dev'| cut -c 23-26 | head -1")
  free = commands.getoutput("df -h | grep '/dev'| cut -c 30-32 | head -1")
  percent = commands.getoutput("df -h | grep '/dev'| cut -c 35-37 | head -1")

  date = commands.getoutput("date")

  rx_wifi = commands.getoutput("cat /sys/class/net/wlan0/statistics/rx_bytes")
  rx_float = float(rx_wifi)
  rx_float_mb = rx_float / 1024 / 1024

  tx_wifi = commands.getoutput("cat /sys/class/net/wlan0/statistics/tx_bytes")
  tx_float = float(tx_wifi)
  tx_float_mb = tx_float / 1024 / 1024
  
  ip_lan = commands.getoutput("ifconfig wlan0 |  grep inet | cut -c 14-26 | head -1")

  status = ({
                  'temperature': temp,
                  'proccess' : quantProc,
                  'memory' : {
                      'total': mem_total,
                      'used' : mem_used,
                      'free' : mem_free
                  },
                  'sdcard' :  {
                      'total' : total,
                      'used' : used,
                      'free' : free,
                      'percent' : percent
                  },
                    'network' :  {
                      'ip_lan' : ip_lan,
                      'network_in' : rx_float_mb,
                      'network_out' : tx_float_mb
                  },
              })
  print(status)
  return jsonify(status = status)
  print('--------------------------------')

@app.route('/api/pins', methods=['GET'])
def getStatePins():

  listapinos = [4, 5, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
  pins = []

  for i in range(len(listapinos)):
    pin = listapinos[i]
    gpio.setup(pin, gpio.OUT)
    state = gpio.input(pin)
    state_pins = {
                  'pin': pin, 
                  'state': state
                  }
    print (state_pins)
    pins.append(state_pins)
    print('--------------------------------')

  return jsonify({'status_pins': pins})

@app.route('/api/pins/<pin>', methods=['GET'])
def setStatePins(pin):

  try:
    pin = int(pin)

  except:
    return jsonify({'state_pins':'Route with invalid pin'})

  gpio.setup(pin, gpio.OUT)
  state = gpio.input(pin)

  try:
    state_pin = isinstance(pin, int)
    pin = int(pin)

    if state_pin == True:
      gpio.setup(pin, gpio.OUT)
      state = gpio.input(pin)

      if state == 0:
        gpio.output(pin, 1)
        state = gpio.input(pin)

      elif state == 1:
        gpio.output(pin, 0)
        state = gpio.input(pin)

      else:
        pass
  except:
    pass

  state_pins = {'pin': pin, 'state': state}
  print (state_pins)
  return jsonify({'state_pins': state_pins})
  print('--------------------------------')


if __name__=='__main__':
  #port = port = int(os.environ.get('PORT', 5050))
  #app.run(debug=True, host='0.0.0.0', port=port)
  app.run()



