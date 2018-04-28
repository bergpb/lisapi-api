# LisaPi

### Api to control state of pins (high, low) and get current system status in your Raspberry PI, over get http methods. 

 First install **gunicorn**:
<code>sudo apt install gunicorn</code>  or <code>pip install gunicorn</code>.

And run this command: 
<code>gunicorn -b 0.0.0.0:8000 wsgi:app</code>

This route return a json with the status of all pins in your Raspberry Pi:
http://192.168.0.1:8000/api/rasp

This route return a json with current system status: 
http://192.168.0.1:8000/api/status

This route set state in your pins, just pass a pin number in url and the server toogle a current pin state:
http://192.168.0.1:8000/api/rasp/pin

Disponible pins to control state (high, low) in Raspberry Pi models B+ and W: <br>
4, 5 ,13 ,16 ,17 ,18 ,19 ,20 ,21 ,22 ,23 ,24 ,25 ,26 and 27.


