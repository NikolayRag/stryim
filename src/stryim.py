#  todo 120 (ui) +0: add ui

import sublime, sublime_plugin
from .muxSink import *
from .muxH264AAC import *
from .mp4Recover import *
from .yiListener import *
from .kiTelnet import *
from .kiLog import *


yiApp= [None] #instance of yiListener


'''
YiOn/Off commands are used to test Stryim in Sublime, `coz its lazy to set up running environment.
'''
class YiOnCommand(sublime_plugin.TextCommand):
	muxers= []	


	def cbConn(self, _mode):
		kiLog.ok('Connected' if _mode else 'Disconnected')

	def cbLive(self, _mode):
		if _mode==1:
			kiLog.ok('Live')
		if _mode==-1:
			kiLog.ok('Dead')
	
	def cbAir(self, _mode):
		if _mode==1:
			kiLog.warn('Air On')
		if _mode==0:
			kiLog.warn('Air Off')
		if _mode==-1:
			kiLog.err('Air bad')

	def cbDie(self):
		for cMux in self.muxers:
			cMux.stop()

		kiLog.ok('off')



	def run(self, _edit):
		kiLog.states(verb=True, ok=True)

		selfIP= KiTelnet.defaults(address='192.168.42.1')

		if yiApp[0]:
			kiLog.warn('Already')
			return

		self.muxers= []

#		self.muxers.append( MuxFLV(SinkTCP(1234), audio=False) )
#		self.muxers.append( MuxAAC(SinkTCP(2345)) )
		self.muxers.append( MuxFLV(SinkFile('D:\\yi\\restore\\stryim\\L.flv'), fps=30000/1001, audio=True, bps=15200) )
#		self.muxers.append( MuxAAC(SinkFile('D:\\yi\\restore\\stryim\\L.aac')) )


		def muxRelay(data):
			for cMux in self.muxers:
				cMux.add(data)
		mp4Restore= Mp4Recover(muxRelay)


		yiApp[0]= YiListener()
		yiApp[0].start(self.cbConn, self.cbLive, self.cbDie)
		yiApp[0].live(mp4Restore.add, self.cbAir)



class YiOffCommand(sublime_plugin.TextCommand):
	def run(self, _edit):
		if not yiApp[0]:
			kiLog.warn('Already')
			return

		yiApp[0].stop()
		yiApp[0]= None
