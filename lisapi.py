# -*- coding: utf-8 -*-

import os
import commands
import RPi.GPIO as gpio
from flask_cors import CORS
from flask import Flask, jsonify

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

@app.route('/api/status', methods=['GET'])
def getStatus():

  status = {}

  temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3

  quantProc = int(commands.getoutput("ps -aux | wc -l"))

  mem_total = int(commands.getoutput("free -h | grep 'Mem' | cut -c 16-18"))
  mem_used = int(commands.getoutput("free -h | grep 'Mem' | cut -c 29-30"))
  mem_free = int(commands.getoutput("free -h | grep 'Mem' | cut -c 40-42"))

  uptime = commands.getoutput("uptime -p")

  total = int(commands.getoutput("df -h | grep '/dev'| cut -c 18-19 | head -1"))
  used = int(commands.getoutput("df -h | grep '/dev'| cut -c 23-25 | head -1"))
  free = int(commands.getoutput("df -h | grep '/dev'| cut -c 30-31 | head -1"))
  percent = commands.getoutput("df -h | grep '/dev'| cut -c 35-36 | head -1")

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

  return jsonify(status = status)

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

    pins.append(state_pins)

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

  return jsonify({'state_pins': state_pins})



if __name__=='__main__':
    app.run()
