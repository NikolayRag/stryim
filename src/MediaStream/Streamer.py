from .Mux import *
from .Sink import *
import logging


#  todo 284 (feature, streaming) +0: Make audio/video mixer (switcher)
'''
Main streaming controller.
Route Atoms from linked Source to managed destination.
'''
class Streamer():
	source= None

	muxer= None

	result= True


	'''
	Init settings.
	Streaming destination will be opened, wainting for muxed Atoms.
	'''
	def __init__(self, _dst, fps=30000./1001):
		self.muxer= self.initMuxer(_dst, fps)



	'''
	Link Source.
	Calling without arguments unlink Source, bu dont close streaming.
	 Other Source can be linked lately.

#  todo 283 (feature, streaming) +0: define Source abstract superclass.
	Source should have .link(atomCB) method.
	'''
	def link(self, _source=None):
		if _source and callable(_source.link):
			_source.link(self.atomPort)
			self.source= _source

		elif self.source:
			self.source.link()
			self.source= None



	'''
	Close destination.
	Streamer is not useful then.
	'''
	def close(self):
		self.muxer.stop()

		self.muxer= None

		return self.result




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
		sink= SinkRTMP

		if protocol[0]!='rtmp':
			if len(protocol)>1 and protocol[0]=='tcp':
				sink= SinkTCP
			else:
				sink= SinkFile

			if len(ext)>1 and (ext[-1]=='264' or ext[-1]=='h264'):
				muxer= MuxH264
			if len(ext)>1 and ext[-1]=='aac':
				muxer= MuxAAC

		return muxer(sink(_dst))




	'''
	Function is passed to Source's link()
	'''
	def atomPort(self, _atom):
		self.muxer.add(_atom)