# OUIcount

## Python programming assignment for Catbird

Status (2014-08-29):  fully implemented.  Good unit test coverage for MAC ingestion, but not for OUI ingestion (which has incomplete error handling).  Functional regression test is not yet automated.  The "oui.txt" reference file is automatically downloaded if it is not present in the current directory.

Deviations from spec:  There are two additional flags, "verbose" and "dontfold", which implement optional behaviors that may be useful for testing.  The field order in "verbose" mode differs from that in default mode, to make it easier to visually scan the counts per OUI.

## Specification

Given the attached list of MAC addresses in base 10, use the oui.txt file at the link provided to determine which organizations have MAC addresses in the list, and how many. 

For instance, the first entry in the macs.txt file is 278159193857459.  If you translate to hex and take the first 6 digits you get FCFBFB.  This corresponds to "CISCO SYSTEMS, INC." in the oui.txt file.  So you'd count one for CISCO SYSTEMS, INC.

Print one organization per line, followed by the number of addresses that organization has in the list. 

Hint: Download the oui.txt file once and read from local file system.  Also all but one of the entries in the macs.txt file has a corresponding company prefix in the oui file.

Here's the link for the oui.txt file:  [oui.txt][1]

[1]: http://standards.ieee.org/develop/regauth/oui/oui.txt
