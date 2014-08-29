#!/usr/bin/python

# test_OUIcount.py - Unit tests for MAC address counting by OUI

import unittest
from OUIcount import *


class TestIngest(unittest.TestCase):
	def setUp(self):
		pass
		
	def test_00001(self):
		self.assertEqual(ingestMAC("00001"), (0, 0, 0, 0, 0, 1))
		
	def test_newline(self):
		self.assertEqual(ingestMAC("00001\n"), (0, 0, 0, 0, 0, 1))
		
	def test_whitespace(self):
		self.assertEqual(ingestMAC("  00001\t  "), (0, 0, 0, 0, 0, 1))
		
	def test_cisco(self):
		self.assertEqual(ingestMAC("278159193857459"), (0xFC, 0xFB, 0xFB, 0xF0, 0xDD, 0xB3))
		
	def test_empty(self):
		with self.assertRaises(ValueError):
			mac = ingestMAC("\n")
			
	def test_nonnumeric(self):
		with self.assertRaises(ValueError):
			mac = ingestMAC("123XX456")
			
	def test_multiline(self):
		with self.assertRaises(ValueError):
			mac = ingestMAC("123\n456")
			
	def test_innerspace(self):
		with self.assertRaises(ValueError):
			mac = ingestMAC("123 456")
			
	def test_toobig(self):
		with self.assertRaises(ValueError):
			mac = ingestMAC("1278159193857459")
			

if __name__ == '__main__':
	unittest.main(verbosity=2)

