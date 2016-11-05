"""This program runs alongside obd_recorder.py (for now) and samples vehicle speed
every 1 second. Eventually, this file should handle everything obd_recorder.py 
does. This file could be written a LOT better. It's kind of a mess right now."""
import os
import time
from datetime import datetime
class logging():
	def __init__(self, path):
		self.savefile = 'rpi_logfile.txt'
		self.path = os.path.dirname(__file__)
		self.filename = path + 'log/log.txt'
		self.f = open(self.filename)
		first = self.f.readline()
		first = first.split(",")
		first[-1] = first[-1].strip()
		num_elements = len(first)
		self.mph_index = first.index("MPH")
		self.time_index = first.index("Time")
	def file_parse(self):	
		i = 0
		f = self.f
		filename = self.filename
		mph_index = self.mph_index
		path = self.path
		for line in f:
			i+=1
		new_last_index = i
		f.close()
		average_time = 0
		while 1:
			y = []
			x = []
			summed_mph = 0
			i = 0
			f = open(filename)
			prev_last_index = new_last_index
			for line in f:
				if i >= prev_last_index:
					line = line.split(",")
					line[-1] = line[-1].strip()
					try: summed_mph += float(line[mph_index])
					except IndexError: i += 0
					except ValueError: i += 0
					i += 1
				else: i += 1
			new_last_index = i
			index_interval = new_last_index - prev_last_index
			self.average_mph = summed_mph / index_interval
			localtime = int(time.time())
			print localtime
			current_time = localtime
			print self.average_mph
			value = str(current_time) + ',' + str(self.average_mph) + '\n'
			with open(path + self.savefile, 'a+') as myfile:
				myfile.write(value)
			f.close()	
			time.sleep(1)
if __name__ == "__main__":
	begin = logging('/home/git/pyobdii/')
	begin.file_parse()
