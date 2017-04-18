'''
Execute telnet command.



class KiTelnet(cmd, callback, address, user, pass, localport, localip)
	Executes 'cmd' in specified telnet.
	To see result, use .result() or provide callback

	cmd
		Default ''
		Command to execute.

	callback(bytestring)
		Function to get partial console output as command is executing.
		if specified, command response is not returned by function itself.

	address
		Default None
		Telnet address.

	user
		Defalt 'root'

	pass
		Default ''

	localport, int
		Params for connecting to self from telnet when using callback.
		Should be firewall-enabled if telnet is remote.

	localip
		Default None.
		Local address for telnet to send results to.
		If not specified, will be tried to detected automatically
		 in same /24 net as specified telnet address.

result()
	Blocking.
	Return console output.
	If 'callback' was provided, empty string will return.
	Object is guaranteed stopped not after result()

	Return False on any error.
'''

import telnetlib, socket, threading

from kiSupport import *
import logging




class KiTelnet():
	tcpSock= None
	blockedFlag= None
	tcpResult= False


	telnetPromptLog= b'login: '
	telnetPromptPass= b'Password: '
	telnetPrompt= b' # '

	telnetAddr= None
	telnetUser= 'root'
	telnetPass= ''
	telnet= None

	selfAddr= None
	selfPort= None



	'''
	find local IP in in the same /24 network as given one
	'''
	@staticmethod
	def localIp(_remoteIP):
		telIPA= str(_remoteIP).split('.')[0:3]

		for cIp in socket.gethostbyname_ex(socket.gethostname())[2]:
			if telIPA== str(cIp).split('.')[0:3]:
				return cIp

		return


	@staticmethod
	def defaults(
		  address=None
		, user=None
		, password=None
		, localport=None
		, localip=None
	):
		if not localip:
			localip= KiTelnet.localIp(address)

		if localip!=None:
			KiTelnet.selfAddr= localip
		if localport!=None:
			KiTelnet.selfPort= localport

		if address!=None:
			KiTelnet.telnetAddr= address
		if user!=None:
			KiTelnet.telnetUser= user
		if password!=None:
			KiTelnet.telnetPass= password

		return (KiTelnet.selfAddr, KiTelnet.selfPort)


	def argsFill(self, _telAddr, _telUser, _telPass, _selfAddr, _selfPort):
		if _telAddr!=None:
			self.telnetAddr= _telAddr
		if self.telnetAddr==None:
			logging.error('missing telnet address')
			return

		if _telUser!=None:
			self.telnetUser= _telUser
		if self.telnetUser==None:
			logging.error('missing telnet user')
			return

		if _telPass!=None:
			self.telnetPass= _telPass
		if self.telnetPass==None:
			logging.error('missing telnet pass')
			return

		if not _selfAddr:
			_selfAddr= KiTelnet.localIp(self.telnetAddr)

		if _selfAddr!=None:
			self.selfAddr= _selfAddr
		if self.selfAddr==None:
			logging.error('missing self address')
			return

		if _selfPort!=None:
			self.selfPort= _selfPort
		if self.selfPort==None:
			logging.error('missing self port')
			return

		return True




	'''
	Constructor.
	Provided command is started to execute without delay.
	Result is fetched with .result(), blocking until command is finished.

	If not provided, telnet and network parameters are taken from defaults,
	 which are set by defaults() static method.
	'''
	def __init__(self
		, _command=''
		, _cbRes=None
		, address=None
		, user=None
		, password=None
		, localport=None
		, localip=None
	):
		self.telnet= telnetlib.Telnet()
		self.blockedFlag= threading.Event()


		if not self.argsFill(address, user, password, localip, localport):
			self.reset()
			return


		if self.tcpPrepare():
			threading.Timer(0, lambda:self.tcpListen(_cbRes)).start()
			threading.Timer(0, lambda:self.tryTelnet(_command)).start()






	def result(self):
		self.blockedFlag.wait();

		return self.tcpResult



	'''
	cancel everything and relax
	'''
	def reset(self, _soft=False):
		if self.tcpSock:
			self.tcpSock.close()
			self.tcpSock= None

		if not _soft:
			self.tcpResult= -1

		self.blockedFlag.set()
		self.telnet.close()











	def tcpPrepare(self):
		self.tcpSock= socket.socket()

		try:
			self.tcpSock.bind((self.selfAddr,self.selfPort))

		except:
			logging.error('Cannot listen to ports: %s' % self.selfPort)

			self.selfPort= None
			self.reset()

			return


		self.tcpSock.listen(1)

		logging.info('Tcp listening to port %s...' % self.selfPort)

		return True


	def tcpListen(self
		, _cbRes=None
		, _timeIn= 2	#not starting within
		, _timeOut= 5	#no output longer than
#  todo 8 (telnet) +0: check for timeout
	):

		tcpTimein= threading.Timer(_timeIn, self.tcpSock.close) #this will raise exception for unresponsive tcpSock
		tcpTimein.start()

		try:
			c, a= self.tcpSock.accept()
		except:
			logging.error('Tcp timeIn')
			self.reset()
			return

		tcpTimein.cancel()
		logging.info('Tcp in from ' +a[0])


		if not _cbRes:
			self.tcpResult= b''
		else:
			self.tcpResult= 0

		while 1:
			iIn= c.recv(16384)
			if not iIn:
				break

			if not _cbRes:
				self.tcpResult+= iIn
			else:
				try:
					_cbRes(iIn)
					self.tcpResult+= len(iIn)
				except:
					logging.error('Tcp callback exception')
					self.tcpResult= -1
					break

		c.close()

		self.reset(True)



	def tryTelnet(self, _command):
		try:
			self.sendTelnet(_command)
		except:
			if not self.blockedFlag.isSet(): #not after end
				logging.error('Telnet error')
				self.reset()


	def sendTelnet(self, _command):
		self.telnet.open(self.telnetAddr)
		logging.info("Telnet running:\n%s" % _command)

		self.telnet.read_until(self.telnetPromptLog)
		self.telnet.write( (self.telnetUser +"\n").encode() )

		if self.telnetPass:
			self.telnet.read_until(self.telnetPromptPass)
			self.telnet.write( (self.telnetPass +"\n").encode() )

		self.telnet.read_until(self.telnetPrompt)
		self.telnet.write( ("(%s)| nc %s %s; exit\n" % (_command, self.selfAddr, self.selfPort)).encode() )
