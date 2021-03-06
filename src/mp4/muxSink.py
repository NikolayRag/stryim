from kiLog import *

'''
Mux-suitable sink for sending binary data to file
'''
class SinkFile():
	cFile= None

	def __init__(self, _fn):
		self.cFile= open(_fn, 'wb')

	def add(self, _data):
		self.cFile.write(_data)

	def close(self):
		self.cFile.close()





'''
Mux-suitable sink for sending binary data to TCP
'''
# -todo 118 (sink) +0: make SinkTCP nonblocking, stream-based
class SinkTCP():
	cSocket= None

	def __init__(self, port, ip='127.0.0.1'):
		self.cSocket= socket.create_connection((ip,port))

		kiLog.ok('Connected to %s, %d' % (ip,port))


	def add(self, _data):
		if not self.cSocket:
			return

		try:
			self.cSocket.sendall(_data)

		except:
			kiLog.err('Socket error')


	def close(self):
		if self.cSocket:
			self.cSocket.close()
			self.cSocket= None




'''
Mux-suitable sink for sending binary data to RTMP
'''
import subprocess, threading, socket
# -todo 119 (sink) +0: make SinkRTMP nonblocking, stream-based
class SinkRTMP():
	rtmp= ''

	tcp= None


	def __init__(self, _rtmp):
		self.rtmp= _rtmp


		ffport= 2345
		threading.Timer(0, lambda: self.serverInit(ffport)).start()
		self.tcp= self.tcpInit(ffport)





	def add(self, _data):
		if not self.tcp:
			return

		try:
			self.tcp.sendall(_data)
		except:
			kiLog.err('Socket error')
			self.tcp= None


	def close(self):
		tcp= self.tcp
		self.tcp= None
		if tcp:
			tcp.close()




	#private

	def serverInit(self, _ffport):
#  todo 104 (clean, release) +0: use 'current' folder for release and hide ffmpeg
#  todo 105 (sink, unsure) -1: hardcode RTMP protocol
		subprocess.call(pyinstRoot('ffmpeg/ffmpeg') +' -i tcp://127.0.0.1:%d?listen -c copy -f flv %s' % (_ffport, self.rtmp), shell=False)


	def tcpInit(self, _ffport):
		return socket.create_connection(('127.0.0.1',_ffport))

