#!/usr/bin/env python

import subprocess
subprocess.Popen('git push', shell=True).wait()
subprocess.Popen('git push staging master', shell=True).wait()
