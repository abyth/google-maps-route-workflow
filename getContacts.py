# -*- coding: utf-8 -*-
import AddressBook
from Cocoa import NSArray
import sys
from unicodedata import normalize
import alfred
import re

query = normalize('NFC', sys.argv[1].decode('utf-8'))

def filterAddress(person): return person.valueForProperty_('Address') != None

def decode(s): return normalize('NFC', unicode(s))

ab = AddressBook.ABAddressBook.sharedAddressBook()

firstName = AddressBook.ABPerson.searchElementForProperty_label_key_value_comparison_(AddressBook.kABFirstNameProperty, None, None, query, AddressBook.kABContainsSubStringCaseInsensitive)
lastName = AddressBook.ABPerson.searchElementForProperty_label_key_value_comparison_(AddressBook.kABLastNameProperty, None, None, query, AddressBook.kABContainsSubStringCaseInsensitive)

firstAndLast = AddressBook.ABSearchElement.searchElementForConjunction_children_(AddressBook.kABSearchOr, NSArray.arrayWithObjects_(firstName, lastName, None))

pl = ab.recordsMatchingSearchElement_(firstAndLast)

pl_filtered = filter(filterAddress, pl)

out = []

for el in pl_filtered:
	uid = decode(el.valueForProperty_('UID'))
	a = el.valueForProperty_('Address')
	for i in range(0, len(a)):
		name = decode(re.sub('[^a-zA-Z1-9]', '', a.labelAtIndex_(i)))
		address = a.valueAtIndex_(i)

		arg =  ""

		if "Street" in address:
			arg += decode(address['Street'])+u","

		if "ZIP" in address:
			arg += decode(address['ZIP'])+u","

		if "City" in address:
			arg += decode(address['City'])

		first = decode(el.valueForProperty_('First'))
		last = decode(el.valueForProperty_('Last'))
		item = alfred.Item(
			attributes = {'uid' : uid, 'arg' : arg},
			title = first + u' ' + last,
			subtitle = name,
			icon = ('public.vcard', {'type': 'filetype'})
		)
		out.append(item)

if len(out) == 0:
	item = alfred.Item(
		attributes = {'uid' : alfred.uid(0), 'arg' : query},
		title = query,
		subtitle = 'Non contact address',
		icon = 'icon.png'
		)
	out.append(item)

xml = alfred.xml(out)
alfred.write(xml)
