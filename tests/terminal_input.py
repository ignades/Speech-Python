#!/usr/bin/python

import subprocess, sys

command = sys.argv[1:]

subprocess.run(command[0], shell = True, executable="/bin/bash")
