import numpy as np
from matplotlib.ticker import PercentFormatter
import pyvisa
import os
from matplotlib.pyplot import  figure, step
from RsInstrument import * 
from datetime import date
import errno
import zipfile
import shutil
import time


rta = None
try:
	rm = pyvisa.ResourceManager()
	rta = rm.open_resource('TCPIP::192.168.100.101::INSTR')
except Exception as ex:
	print('Error initializing the instrument session:\n' + ex.args[0])
	exit()

rta.close()