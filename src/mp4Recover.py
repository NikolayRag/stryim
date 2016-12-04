import subprocess, tempfile, re

from .byteTransit import *
from .kiLog import *


class AtomMatch():
	typeMoov= False
	typeAVC= False
	typeAAC= False
	AVCKey= None
	inPos= None
	outPos= None

	def __init__(self, _in, _out):
		self.inPos= _in
		self.outPos= _out

	def setMOOV(self):
		self.typeMoov= True
		self.typeAVC= False
		self.typeAAC= False

		return self


	def setAVC(self, _key=False):
		self.typeMoov= False
		self.typeAVC= True
		self.typeAAC= False
		self.AVCKey= _key

		return self


	def setAAC(self):
		self.typeMoov= False
		self.typeAVC= False
		self.typeAAC= True

		return self


class Atom():
# -todo 124 (recover, mp4) +0: change Atom fields to data plus atom-specific structures
	type= None
	data= None

	def __init__(self, _type=None, _data=b''):
		self.type= _type
		self.data= _data



# =todo 101 (recover) +2: use native atoms searching: [h264, aac, ...]
class Mp4Recover():
	h264Presets= {
		  (1080,30,0): b'\'M@3\x9ad\x03\xc0\x11?,\x8c\x04\x04\x05\x00\x00\x03\x03\xe9\x00\x00\xea`\xe8`\x00\xb7\x18\x00\x02\xdcl\xbb\xcb\x8d\x0c\x00\x16\xe3\x00\x00[\x8d\x97ypxD"R\xc0'
		, -1: b'\x28\xee\x38\x80'
	}


	transit= None
	atomCB= 	None


	def __init__(self, _atomCB):
		self.transit= byteTransit(self.atomsFromRaw, 500000)


		self.atomCB= _atomCB

		if callable(self.atomCB):
			self.atomCB( Atom('IDR', self.h264Presets[(1080,30,0)]) )
			self.atomCB( Atom('IDR', self.h264Presets[-1]) )
		

	def add(self, _data, _ctx=None):
		self.transit.add(_data, _ctx)




	'''
	Provide raw mp4 data to parse in addition to allready provided.
	Return numer of bytes actually consumed.

		data
			.mp4 byte stream data

		finalize
			boolean, indicates no more data for this context will be sent (if consumed all).
	'''
# -todo 123 (clean) +0: remove ctx arg
	def atomsFromRaw(self, _data, _ctx, _finalize=False):
		recoverMatchesA= self.analyzeMp4(_data)


		kiLog.ok("%d matches" % len(recoverMatchesA))


		dataCosumed= 0
		for match in recoverMatchesA:
			restoredData= _data[ match['offset'] : match['len'] ]
			self.atomCB( Atom(match['type'],restoredData) )

			dataCosumed= match['offset'] +match['len']


		return dataCosumed



	'''
	Search .mp4 bytes for 264 and aac frames.
	Return Atom() array.
	
	First frame searched is IDR (Key frame).
	Last frame is the one before last found IDR frame, or before MOOV atom if found.

	If called subsequently on growing stream, 2nd and next call's data[0] will point to IDR.
	'''
	def analyzeMp4(self, _data):
		signMoov= b'\x6d\x6f\x6f\x76'
		signAAC= b'\x21' #aac
		signA= [b'\x25\xb8\x01\x00', b'\x21\xe0\x10\x11', b'\x21\xe0\x20\x21', b'\x21\xe0\x30\x31', b'\x21\xe0\x40\x41', b'\x21\xe0\x50\x51', b'\x21\xe0\x60\x61', b'\x21\xe0\x70\x71']
		signI= 0
		signI1= 1 #cached version


		'''
		Detects Atom assumed to be started from _in.
		Return: Atom if detected, False if not, or None if insufficient data.
		_in must be not less than 4.
		
		AVC: 4b:size, size:(signA[x],...), signAAC|(4b,signA[x+1])|(4b,signMoov)
		AAC: signAAC, ?:..., (4b,signA[x+1])|(4b,signMoov)
		MOOV: 4b:size, signMoov
		'''
		def analyzeAtom(_data, _inPos, _signAVC, _signAVC1):
			if (_inPos+8)>len(_data):	#too short for anything
				return None


			#AVC/MOOV
			signThis= _data[_inPos+4:_inPos+8]
			outPos= _inPos +4 +int.from_bytes(_data[_inPos:_inPos+4], 'big')


			if signThis==signMoov:
				if outPos>len(_data): #Not enough data to test
					return None

				return AtomMatch(_inPos,outPos).setMOOV()


			if signThis==_signAVC:
				if (outPos+8)>len(_data): #Not enough data to test
					return None

				signNext= _data[outPos+4:outPos+8]
				if (
					   signNext!=_signAVC1
					and signNext!=signMoov
					and _data[outPos]!=signAAC[0]
				):
					return False

				return AtomMatch(_inPos,outPos).setAVC(signThis==signA[0])


			#AAC
			if _data[_inPos]==signAAC[0]:
				outPos= _data.find(_signAVC, _inPos)-4


				moovStop= outPos
				if outPos<0:
					moovStop= len(_data)

				moovPos= _data[_inPos:moovStop].find(signMoov)
				if moovPos>=0:	#MOOV found ahead
					outPos= _inPos+moovPos-4


				if outPos<0:	#still nothing found
					return None

				return AtomMatch(_inPos,outPos).setAAC()


			return False






		KFrameLast= None	#Last IDR frame to cut out if not finalize
		matchesA= []

		'''
		search: AVC-Key, ([AAC,AVC|AVC], ...)
		'''
		foundStart= 0
		while True:
			atomMatch= analyzeAtom(_data, foundStart, signA[signI], signA[signI1])
			if atomMatch==None: #not enough data, stop
				break

			if atomMatch==False: #retry further
				kiLog.warn('Wrong atom, research')
				foundStart= _data.find(signA[signI], foundStart+1+4)-4	#rewind to actual start
				if foundStart<0:	#dried while in search
					break

				continue


			#Atom found
			if atomMatch.typeMoov:	#abort limiting
				KFrameLast= None
				break


			matchesA.append(atomMatch)

			foundStart=	atomMatch.outPos	#shortcut for next


			if atomMatch.typeAVC:
				signI= signI1

				signI1+= 1
				if signI1==len(signA):
					signI1= 0


				if atomMatch.AVCKey:	#limits to keyframes
					KFrameLast= len(matchesA)-1



		kiLog.verb('%d atoms found%s' % (len(matchesA)-(KFrameLast or 0), ', finaly' if not KFrameLast else ''))

		return matchesA[:KFrameLast]








import sublime, sublime_plugin

class YiTestCommand(sublime_plugin.TextCommand):
	def run(self, _edit):
		f= open('e:/yi/L0010840.MP4', 'rb')
		b= f.read()
		f.close()

		print( Mp4Recover(None).analyzeMp4(b) )
