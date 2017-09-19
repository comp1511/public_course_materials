#!/usr/bin/python
# Written by andrewt@cse.unsw.edu.au  for COMP2041
# Simple cp implementation by running /bin/cp

import sys,subprocess
if len(sys.argv) != 3:
    sys.stderr.write("Usage: %s <enrollment_file> <course_codes>\n" % sys.argv[0])
    sys.exit(1)
subprocess.call(['cp', sys.argv[1], sys.argv[2]])