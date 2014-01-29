# -*- coding: utf-8 -*-
from CoreLocation import CLLocationManager
from Cocoa import (NSObject, NSRunLoop, NSDefaultRunLoopMode, NSDate, NSThread)
import sys
import webbrowser
import time
from unicodedata import normalize
import alfred

def decode(s): return normalize('NFC', s.decode('utf-8'))

target = decode(sys.argv[1])

url = u"https://maps.google.de/maps?saddr={latitude},{longitude}&daddr={target}"

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

clm = LocationManager.alloc().init_with_thread(NSThread.currentThread())

loop = NSRunLoop.currentRunLoop()

loop.runMode_beforeDate_(NSDefaultRunLoopMode, NSDate.distantFuture())

loc = clm.goodLocation

if loc != None:
	url = url.replace(u"{latitude}", unicode(loc.coordinate().latitude))
	url = url.replace(u"{longitude}", unicode(loc.coordinate().longitude))
	url = url.replace(u"{target}", target)

	webbrowser.open(url.encode('utf-8'))
clm.dealloc()
