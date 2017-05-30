from .Atom import *
from .Mux import *
from .Sink import *
try:
	from Stat import *
except:
	from src.Stat import *

import threading, queue
import logging


#  todo 284 (feature, streaming) +0: Make audio/video mixer (switcher) as a Source-to-Streamer fabric
'''
Main streaming controller.
Route Atoms from linked Source to managed destination.
'''
class Streamer(threading.Thread):
	stat= None

	source= None

	muxer= None
	sink= None
	atomsQ= None

	live= True


	'''
	Init settings.
	Streaming destination will be opened, wainting for muxed Atoms.
	'''
	def __init__(self):
		threading.Thread.__init__(self)

		self.stat= Stat()
		self.stat.trigger(StatTrigger(fn=self.stat.max, steps=[10,20,30,50,80,130,200,350,550,900,1500,2300,3800,6100,10000], cb=self.statCB))

		self.atomsQ= queue.Queue()

		self.start()



	def begin(self, _dst, fps=30000./1001):
		if self.muxer:
			logging.warning('Stream already running')
			return

		self.muxer= self.initMuxer(_dst, fps)

		logging.info('Streaming to %s' % _dst)

		return True



	'''
	(re)Link Source.
	Calling without arguments unlink Source without stopping streaming.
	 Other Source can be linked lately.

#  todo 283 (feature, streaming) +0: define Source abstract superclass.
	Source should have .link(atomCB) method.
	'''
	def link(self, _source=None):
		self.source and self.source.link()

		if _source and callable(_source.link):
			_source.link(self.atomPort)
			self.source= _source



	'''
	Close destination.
	'''
	def end(self):
		self.muxer and self.muxer.stop()
		self.muxer= None

		logging.info('Closed')



	'''
	Close and stop streamer.
	It cant be restarted.
	'''
	def kill(self):
		self.end()
		
		self.live= False



### PRIVATE



	'''
	Create muxer and sink based on destination.
	
	Set FLV/rtmp general streaming if destination begins with 'rtmp://..'.
	'tcp://..' tells to send over TCP, which is suitable with ffmpeg.
	Otherwise destination should be valid file path to save.

	For non-rtmp desstination use ['.FLV'|'.264'|'.AAC'] extension
	 to define output format.
	'''
	def initMuxer(self, _dst, _fps):
		_dst= '/'.join(_dst.split('\\'))
		protocol= _dst.split(':/')
		ext= _dst.split('.')


		MuxFLV.defaults(fps=_fps, srate=48000)
		muxer= MuxFLV
		sink= SinkNet

		if protocol[0] not in ['rtmp', 'udp', 'tcp']:
			if protocol[0] in ['srv']:
				sink= SinkServer
			else:
				sink= SinkFile

				if len(ext)>1 and (ext[-1] in ['264', 'h264']):
					muxer= MuxH264
				if len(ext)>1 and ext[-1]=='aac':
					muxer= MuxAAC

# =todo 307 (streaming, mux, sink) +0: Get stream prefix from source
		h264= {
		  	(1080,2997,0): b'\'M@3\x9ad\x03\xc0\x11?,\x8c\x04\x04\x05\x00\x00\x03\x03\xe9\x00\x00\xea`\xe8`\x00\xb7\x18\x00\x02\xdcl\xbb\xcb\x8d\x0c\x00\x16\xe3\x00\x00[\x8d\x97ypxD"R\xc0'
			, -1: b'\x28\xee\x38\x80'
		}

		self.sink= sink(_dst, muxer.makeHeader([h264[(1080,2997,0)], h264[-1]]))
		return muxer(self.sink)




	'''
	Function is passed to Source's link()
	'''
	def atomPort(self, _atom):
		if isinstance(_atom, Atom):
			self.atomsQ.put(_atom)

			self.stat.add(self.atomsQ.qsize())

	

	'''
	Thread cycle.
	Spool Atoms queue to muxer+sink
	'''
	def run(self):
		while self.live:
			cAtom= None
			try:
				cAtom= self.atomsQ.get(timeout=.1)
			except queue.Empty:
				pass


			if self.muxer:
				if not self.sink.live():
					logging.error('Sink is dead')
			
					self.end()

				elif cAtom:
					self.muxer.add(cAtom)


			self.stat.add(self.atomsQ.qsize())



	'''
	Get statistic
	'''
	def statCB(self, _val, _raise):
		if _raise:
			if _val==750:
				logging.error('Low streaming bandwidth, data is jammed')
				
			logging.debug('Atoms over: %s' % _val)
		else:
			logging.debug('Atoms under: %s' % _val)
