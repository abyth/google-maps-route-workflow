# -*- coding: utf-8 -*-
from CoreLocation import CLLocationManager
from Cocoa import (NSObject, NSRunLoop, NSDefaultRunLoopMode, NSDate, NSThread)
import sys
import time
from unicodedata import normalize
import alfred
import subprocess

def decode(s): return normalize('NFC', s.decode('utf-8'))

vendors = { 'google' : u"https://maps.google.de/maps?saddr={source}&daddr={destination}",
			'apple' :  u"https://maps.apple.com/?saddr={source}&daddr={destination}"}

class LocationManager(NSObject):

	def init_with_thread(self, thread):
		self = super(LocationManager, self).init()
		self.lm = CLLocationManager.alloc().init()
		self.thread = thread
		self.goodPositionFound = False
		self.goodLocation = None
		self.lm.setDelegate_(self)
		self.lm.startUpdatingLocation()
		
		return self

	def locationManager_didUpdateToLocation_fromLocation_(self, manager, newLocation, oldLocation):
		# Ignore updates where nothing we care about changed
		if newLocation is None:
			return

		if self.goodLocation != None:
			return

		if newLocation.horizontalAccuracy() <= 100:
			self.goodLocation=newLocation
			self.lm.stopUpdatingLocation()
			self.goodPositionFound = True
			self.performSelector_onThread_withObject_waitUntilDone_("wakeUp", self.thread, None, False)
		return

	def locationManager_didFailWithError_(self, manager, error):
		print "Could not find current location: " +error
		self.lm.stopUpdatingLocation()
		self.lm.dealloc()
		exit(1)

	def wakeUp(self):
		pass

query = decode(sys.argv[1])

f = open('vendor')
try:
	url = vendors[f.readline().rstrip()]
except Exception, e:
	url = vendors['google']
	f.close()	

dests = filter(lambda x:x!=u"", query.split(';',1))

if len(dests)<2:
	clm = LocationManager.alloc().init_with_thread(NSThread.currentThread())

	loop = NSRunLoop.currentRunLoop()

	loop.runMode_beforeDate_(NSDefaultRunLoopMode, NSDate.distantFuture())

	loc = clm.goodLocation

	if loc != None:
		latitude = unicode(loc.coordinate().latitude)
		longitude = unicode(loc.coordinate().longitude)
	clm.dealloc()
	if query.index(';') < 2:
		url = url.replace(u"{source}",latitude + u"," + longitude)
		url = url.replace(u"{destination}", dests[0])
	else: 
		url = url.replace(u"{destination}",latitude + u"," + longitude)
		url = url.replace(u"{source}", dests[0])
else:
	url = url.replace(u"{source}", dests[0])
	url = url.replace(u"{destination}", dests[1])

subprocess.call(['open', url])

