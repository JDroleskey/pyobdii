"""This program will be used to calculate average speed within a given timeframe. 
Eventually, I'll also probably use this program to calculate MPG from speed and 
Mass Air Flow, once I figure out how to pull MAF from the OBDII port (the pyobd
libraries say that it is not supported on my car)
"""

class data():
	def __init__(self, path):
		self.filename = path + 'SpeedvsTime.txt'
		timeframe_start = str(input("Starting time for analysis: "))
		timeframe_end = str(input("Ending time for analysis: "))
		i = 0
		divisor = 0
		self.timeframe = []
		start_index = None
		end_index = None
		f = open(self.filename)
		for line in self.f:
			if line.find(timeframe_start) != -1:
				start_index = i
			if start_index != None and end_index != None:
				break
			elif line.find(timeframe_end) != -1:
				end_index = i
			elif start_index != None and end_index == None:
				line = line.split(',')[1]
				self.timeframe.append(line.strip('\n'))
			i += 1
		self.divisor = end_index - start_index
	def average_mph(self):
		average = 0
		for speed in self.timeframe:
			average += float(speed)
		self.average_mph = average/self.divisor
		print "The average speed in this timeframe was: " + str(self.average_mph) + " miles per hour."
if __name__ == "__main__":
	speed = data('/home/git/pyobdii/')
	speed.average_mph()
