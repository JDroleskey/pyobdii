import obd_io
import serial
import platform
import obd_sensors
from datetime import datetime
import time
from obd_utils import scanSerial

class OBD_Logger():
	def __init__(self, path, log_items):
		self.port = None
		self.sensorlist = []
		filename = path + "SpeedvsTime.txt"
		self.log_file = open(filename, "w", 128)
		self.log_file.write("Time,MPH\n")
		for item in log_items:
			self.add_log_item(item)
		
	def connect(self):
		portnames = scanSerial()
		print portnames
		for port in portnames:
			self.port = obd_io.OBDPort(port, None, 2, 2)
			if self.port.State == 0:
				self.port.close()
				self.port = None
			else: break
		
		if self.port:
			print "Connected to port " + self.port.port.name
			
	def is_connected(self):
		return self.port
		
	def add_log_item(self, item):
		for index, e in enumerate(obd_sensors.SENSORS):
			if item == e.shortname:
            	#print index
            	self.sensorlist.append(index)
            	print "Logging item: "+e.name
            	break
	
	def record_data(self):
		if self.port is None: return None
		
		print "Logging started"
		print self.sensorlist
		while 1:
		#This is gonna need to be fixed eventually because the format looks like shit
			localtime = time.localtime()[3:6]
			current_time = str(localtime[0]) + ':' + str(localtime[1]) + ':' + str(localtime[2])
			log_string = current_time
			results = {}
		for index in self.sensorlist:
			(name, value, unit) = self.port.sensor(index)
			log_string = log_string + ","+str(value)
			results[obd_sensors.SENSORS[index].shortname] = value
		print log_string
		self.log_file.write(log_string + '\n')
	def calculate_mph(self, speed):
		if speed == "" or speed == 0:
			return 0
		mph = (speed*1.609*1000)
		
logitems = ["speed"]
o = OBD_Logger('/home/git/pyobdii/log/', logitems)
o.connect()
if not o.is_connected(): print "Not connected"
o.record_data()
				
				
