def getA(_var, _field, _default=False):
	if not isinstance(_var, dict):
		return _default

	if not _field in _var:
		return _default

	return _var[_field]


def pad(_val, _pad=4):
	_val= str(_val)
	valLen= min(len(_val),_pad)

	return '0'*(_pad-valLen) +_val[-valLen:]

def bitsCollect(_bitPairs, _int=False):
	rlen= 0
	result= 0
	for cLen,cVal in _bitPairs:
		result= (result<<cLen) +cVal
		rlen+= cLen

	if _int:
		return result

	return result.to_bytes(int(rlen/8)+(rlen%8>0), 'big')



def clip(_val, _from, _to):
	if _val<_from:
		return _from

	if _val>_to:
		return _to

	return _val



class Bits():
	gen= None

	left= 0
	got= 0


	def __init__ (self, _data=b''):
		self.left= len(_data) +1
		self.got= 0
		self.gen= self.bitGen(_data)


	def get (self, _num):
		out= 0

		for i in range(_num):
			out= out<<1
			if self.left:
				try:
					out+= next(self.gen)
				except:
					self.left= 0

		return out


	def bitGen (self, _bytes):
		for b in _bytes:
			self.left-= 1
			self.got+= 1
			for i in range(7,-1,-1):
				yield (b >> i) & 1
