 # -*- coding: utf-8 -*-
import AddressBook
from Cocoa import NSArray
import sys
from unicodedata import normalize
import alfred
import re

def filterAddress(person): return person.valueForProperty_('Address') != None

def decode(s): return normalize('NFC', unicode(s))

def normalize_list(l): return map(lambda x: normalize('NFC', x), map(lambda x: x.decode('utf-8'), l))

query = normalize_list(sys.argv)

ab = AddressBook.ABAddressBook.sharedAddressBook()

addrs = []

flag = True
flag2 = True

for i in range(1,len(query)):
	firstName = AddressBook.ABPerson.searchElementForProperty_label_key_value_comparison_(AddressBook.kABFirstNameProperty, None, None, query[i], AddressBook.kABContainsSubStringCaseInsensitive)
	lastName = AddressBook.ABPerson.searchElementForProperty_label_key_value_comparison_(AddressBook.kABLastNameProperty, None, None, query[i], AddressBook.kABContainsSubStringCaseInsensitive)

	firstAndLast = AddressBook.ABSearchElement.searchElementForConjunction_children_(AddressBook.kABSearchOr, NSArray.arrayWithObjects_(firstName, lastName, None))

	pl = ab.recordsMatchingSearchElement_(firstAndLast)

	pl_filtered = filter(filterAddress, pl)

	src = []

	for el in pl_filtered:
		uid = decode(el.valueForProperty_('UID'))
		a = el.valueForProperty_('Address')
		for i in range(0, len(a)):
			name = decode(re.sub('[^a-zA-Z1-9]', '', a.labelAtIndex_(i)))
			address = a.valueAtIndex_(i)

			addr =  ""

			if "Street" in address:
				addr += decode(address['Street'])+u","

			if "ZIP" in address:
				addr += decode(address['ZIP'])+u","

			if "City" in address:
				addr += decode(address['City'])

			first = decode(el.valueForProperty_('First'))
			last = decode(el.valueForProperty_('Last'))

			src.append({"first": first, "last":last, "addr": addr, "type": name})
	addrs.append(src)

if addrs[0] == []:
	addrs[0] = query[1]
	flag = False

if len(query) > 2 and addrs[1] == []:
	addrs[1] = query[2]
	flag2 = False

out = []

if len(query)<3:
	if flag:
		for pl in addrs[0]:	
			item = alfred.Item(
				attributes = {'uid' : alfred.uid(0), 'arg' : u";"+pl["addr"]},
				title = u"Position -> " + pl["first"] + u" " + pl["last"],
				subtitle = pl["type"],
				icon = ('public.vcard', {'type': 'filetype'})
				)
			out.append(item)
			item = alfred.Item(
				attributes = {'uid' : alfred.uid(0), 'arg' : pl["addr"]+u";"},
				title = pl["first"] + u" " + pl["last"] + u" -> Position",
				subtitle = pl["type"],
				icon = ('public.vcard', {'type': 'filetype'})
				)
			out.append(item)
	else:
		item = alfred.Item(
			attributes = {'uid' : alfred.uid(0), 'arg' : u";"+addrs[0]},
			title = u"Position -> " + addrs[0],
			subtitle = u"Non contact address",
			icon = 'icon.png'
			)
		out.append(item)
		item = alfred.Item(
			attributes = {'uid' : alfred.uid(0), 'arg' : addrs[0]+u";"},
			title = addrs[0] + u" -> Position",
			subtitle = u"Non contact address",
			icon = 'icon.png'
			)			
		out.append(item)
else:
	if flag:
		for pl in addrs[0]:
			if flag2:
				for pl2 in addrs[1]:
					if pl == pl2 : break
					item = alfred.Item(
						attributes = {'uid' : alfred.uid(0), 'arg' : pl["addr"]+ u";" + pl2["addr"]}, 
						title = pl["first"] + u" " + pl["last"] + u" -> " + pl2["first"] + u" " + pl2["last"], 
						subtitle = pl["type"] + u" -> " + pl2["type"], 
						icon = ('public.vcard', {'type': 'filetype'})
						)
			else:
				item = alfred.Item(
					attributes = {'uid' : alfred.uid(0), 'arg' : pl["addr"]+ u";" + addrs[1]}, 
					title = pl["first"] + u" " + pl["last"] + u" -> " + addrs[1], 
					subtitle = pl["type"] + u" -> Non contact address", 
					icon = ('public.vcard', {'type': 'filetype'})
					)
			out.append(item)				
	else:
		if flag2:
			for pl2 in addrs[1]:
				item = alfred.Item(
					attributes = {'uid' : alfred.uid(0), 'arg' : addrs[0] + u";" + pl["addr"]}, 
					title = addrs[0] + u" -> " + pl["first"] + u" " + pl["last"], 
					subtitle = u"Non contact address -> " + pl2["type"], 
					icon = ('public.vcard', {'type': 'filetype'})
					)
				out.append(item)					
		else:
			item = alfred.Item(
				attributes = {'uid' : alfred.uid(0), 'arg' : addrs[0]+ u";" + addrs[1]},
				title = addrs[0] + u" -> " + addrs[1],
				subtitle = u"Non contact address -> Non contact address",
				icon = 'icon.png'
				)	
			out.append(item)

xml = alfred.xml(out)
alfred.write(xml)
