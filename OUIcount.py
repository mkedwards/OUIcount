#!/usr/bin/python

# OUIcount.py - Count MAC addresses (given as decimal numbers) by OUI

# Note that the omission of docstrings is intentional.  I often don't document/comment code
# until there's a human code reviewer in the loop, or at least an automated documentation
# extractor/prettyprinter.  I'm not currently tooled up to run Doxygen on this code.
#
# The exception is when I'm using doctest to embed unit tests in docstrings.  I think that's
# generally a good approach, and that well-written tests should illustrate the design intention
# without a whole lot of verbiage.  The plain English documentation should be written to provide
# readability (and add theory of operation) for the series of tests.  (I'm also a believer in test
# coverage analysis - preferably at the level of branch coverage as well as line coverage - not
# least because a test suite with full branch coverage is a highly effective specification for
# the intended behavior of the implementation.)

from __future__ import print_function
import sys
import argparse
from collections import defaultdict, namedtuple
import os.path
import wget


# The order of fields in the named tuple definition determines the sort order.
OUI = namedtuple('OUI', ['is_unknown', 'name', 'prefix'])


def ingestMAC(s):
	trimmed = s.split()
	l = len(trimmed)
	if l != 1:
		raise ValueError('expected exactly one string of digits in "%s", found %d' % (s, l))
	decimal = trimmed[0]
	if not decimal.isdigit():
		raise ValueError('found non-digit in "%s"' % (decimal,))
	n = long(decimal)
	b = []
	for i in range(0, 6):
		b.append(n % 0x100)
		n >>= 8
	if n != 0:
		raise ValueError('numeric value of "%s" exceeds MAC range (6 bytes)')
	return tuple(b[::-1])


prefix_to_name = {}

def loadOUIs():
	global prefix_to_name
	if not os.path.isfile('oui.txt'):
		wget.download('http://standards.ieee.org/develop/regauth/oui/oui.txt', bar=wget.bar_thermometer)
	f = open('oui.txt', 'r')
	for line in f:
		if line.find('(hex)') == -1:
			continue
		(text_prefix, _, name) = line.strip().split(None, 2)
		prefix = tuple(int(xx, 16) for xx in text_prefix.split('-'))
		if len(prefix) != 3:
			raise ValueError('"%s" is not a valid MAC address prefix' % (text_prefix,))
		prefix_to_name[prefix] = name


known_prefixes = {}

def lookupOUI(prefix, dontfold):
	global known_prefixes
	oui = known_prefixes.get(prefix)
	if oui is None:
		name = prefix_to_name.get(prefix)
		if name is None:
			name = '(unknown) %02X:%02X:%02X' % prefix
			oui = OUI(True, name, prefix)
		elif dontfold:
			oui = OUI(False, name, prefix)
		else:
			oui = OUI(False, name, (0, 0, 0))
		known_prefixes[prefix] = oui
	return oui


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Count MAC addresses (given as decimal numbers) by OUI')
	parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
	                    help='verbose (enumerate MACs per OUI)')
	parser.add_argument('-d', '--dontfold', dest='dontfold', action='store_true',
	                    help='don\'t fold prefixes with identical OUI strings')
	parser.add_argument('MACfile', type=argparse.FileType('r'),
	                    help='file containing decimal MAC addresses')
	# Command line arguments are hard-coded for convenience of testing on iOS with Pythonista
	args = parser.parse_args(['macs.txt'])

	loadOUIs()

	count_by_oui = defaultdict(int)
	if args.verbose:
		macs_by_oui = defaultdict(list)

	line_count = 0
	mac_count = 0
	unknown_count = 0

	for line in args.MACfile:
		line_count += 1
		if line.isspace():
			continue
		mac = ingestMAC(line)
		oui = lookupOUI(mac[0:3], args.dontfold)
		count_by_oui[oui] += 1
		mac_count += 1
		if oui.is_unknown:
			unknown_count += 1
		if args.verbose:
			macs_by_oui[oui].append(mac)

	for oui, count in sorted(count_by_oui.items()):
		if args.verbose:
			print('%d\t%s' % (count_by_oui[oui], oui.name))
			for mac in sorted(macs_by_oui[oui]):
				print('\t%02X:%02X:%02X:%02X:%02X:%02X' % mac)
		else:
			print('%s\t%d' % (oui.name, count_by_oui[oui]))
		
	if args.verbose:
		print('\n%d MACs (%d with unknown OUI) in %d lines' % (mac_count, unknown_count, line_count))
