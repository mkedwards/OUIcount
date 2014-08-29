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


# The order of fields in the named tuple definition determines the sort order.
OUI = namedtuple('OUI', ['is_known', 'name', 'prefix'])


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


def loadOUIs():
	# XXX Load reference OUI index from oui.txt
	pass


known_prefixes = {}

def lookupOUI(prefix):
	global known_prefixes
	oui = known_prefixes.get(prefix)
	if oui is None:
		# XXX Look up prefix in reference OUI index
		name = '(unknown) %02X:%02X:%02X' % prefix
		oui = OUI(False, name, prefix)
		known_prefixes[prefix] = oui
	return oui


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Count MAC addresses (given as decimal numbers) by OUI')
	parser.add_argument('-v', dest='verbose', action='store_true',
	                    help='verbose (enumerate MACs per OUI)')
	parser.add_argument('MACfile', type=argparse.FileType('r'),
	                    help='file containing decimal MAC addresses')
	# Command line arguments are hard-coded for convenience of testing on iOS with Pythonista
	args = parser.parse_args(['-v', 'macs.txt'])

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
		oui = lookupOUI(mac[0:3])
		count_by_oui[oui] += 1
		mac_count += 1
		if not oui.is_known:
			unknown_count += 1
		if args.verbose:
			macs_by_oui[oui].append(mac)

	for oui, count in sorted(count_by_oui.items()):
		print('%d\t%s' % (count_by_oui[oui], oui.name))
		if args.verbose:
			for mac in sorted(macs_by_oui[oui]):
				print('\t%02X:%02X:%02X:%02X:%02X:%02X' % mac)

	if args.verbose:
		print('\n%d MACs (%d with unknown OUI) in %d lines' % (mac_count, unknown_count, line_count))
