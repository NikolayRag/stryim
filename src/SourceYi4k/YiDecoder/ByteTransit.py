import io

'''
Manage context-grouped chunks of byte data.
Data is added to active chunks, splitted by context and then
 sequentally dispatched to callback function.


ByteTransit(cb, trigger)
	Caches added data and dispatch it, respecting consumed ammount. 


	cb(data, forced)
		Dispatch callback.
		Should return ammount of bytes consumed,
		 remaining chunk will be shifted that size.
		Dispatch is forced when context changes. It will be called in a cycle
		 while remaining context is not dried up.

		
	trigger
		Size of data available in chunk for dispatch callback to take place.
		Zero for immediate dispatch.


add(data, ctx)
	Add binary data to ctx context.
	Switching context forces remaining all data to be dispatched
	 implying it is all consumed. 



'''
class ByteTransitChunk():
	dataIO = None

	def __init__(self):
		self.dataIO = io.BytesIO(b'')


	def add(self, _data):
		self.dataIO.write(_data)


	def read(self):
		self.dataIO.seek(0)
		return self.dataIO.read()


	def shrink(self, _amt):
		self.dataIO.seek(_amt)
		data= self.dataIO.read()

		self.dataIO = io.BytesIO(b'')
		self.dataIO.write(data)




class ByteTransit():
	chunk= False
	context= None

	dispatchCB= None
	trigger= 0
	

	def __init__(self, _dispatchCB, _trigger=0):
		self.dispatchCB= callable(_dispatchCB) and _dispatchCB
		self.trigger= _trigger

		self.chunk= ByteTransitChunk()



	def add(self, _data, _ctx=None):
		if self.context!=_ctx:
			self.context= _ctx
			self.dispatch(True)
			


		if _data:
			self.chunk.add(_data)

			self.dispatch()



	#private

	def dispatch(self, _force=False):
		dataLeft= self.chunk.read()


		if not _force:
			if not len(dataLeft) or len(dataLeft)<self.trigger:
				return 0


		dispatched= self.dispatchCB and self.dispatchCB(dataLeft, _force)

		if dispatched:
			self.chunk.shrink(dispatched)
