import serial
import glob
import sys

print "hi"
running = 1

def serial_ports():
	if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
	        # this excludes your current terminal "/dev/tty"
	        ports = glob.glob('/dev/tty[A-Za-z]*')

	result = []
	portArduino = ""
	for port in ports:
	    try:
	        s = serial.Serial(port)
	        s.close()
	        result.append(port)
	        if port.find("ACM") != -1:
	        	portArduino = port
	    except (OSError, serial.SerialException):
	        pass
	    return portArduino

if __name__ == "__main__":
	print(serial_ports())
	ser = serial.Serial(serial_ports())

	while running == 1:
		try :
			line = ser.readline()
		 	print line
		except KeyboardInterrupt:
			running = 0
			print "Session ended"
			ser.close()

	# while True:
	# 	line = ser.readline()
	# 	print line

	# with serial.Serial('/dev/ttyS1', 9600, timeout=1) as ser:
	# 	line = ser.readline()   # read a '\n' terminated line
	# 	print line