#!/usr/bin/env python3

import os
import sys

exec = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'server', 'kt')

os.chdir(os.path.dirname(exec))
os.execv(exec, [exec] + sys.argv[1:])
