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
import matplotlib.pyplot as plt

rm = pyvisa.ResourceManager()
rta = rm.open_resource('TCPIP::192.168.100.101::INSTR')
arbGen = rm.open_resource('TCPIP::192.168.100.103::INSTR')

#dec=[100e3, 200e3, 300e3, 400e3, 500e3, 600e3, 700e3, 800e3, 900e3, 1000e3, 2000e3, 3000e3, 4000e3, 50000e3, 6000e3, 7000e3, 8000e3, 9000e3, 10000e3]
vpp = []
fc=3.4e6
wc=2*np.pi*fc
f = np.linspace(100e3, 10e6, num=500)
w=2*np.pi*f
h_wj = wc/(w*1j+wc)
mag_h_wj= abs(h_wj)
fig , axes = plt.subplots()
axes.semilogx(f, mag_h_wj )
axes.grid(True)
axes.set_xlabel("Frecuencia (Hz)")
axes.set_ylabel("Ganancia (V)")



arbGen.write("C1:BSWV WVTP,SINE")
arbGen.write("C1:BSWV AMP,2.940")
arbGen.write("C1:BSWV WIDTH,1e-6")
rta.write("MEAS1:MAIN PEAK")

for i in range(len(f)):   
    arbGen.write("C1:BSWV FRQ,"+str(f[i]))
    if arbGen.query("*OPC?") != 1:
        time.sleep(0.1)
    vpp.append(float(rta.query("MEAS1:RES:ACTual?")))
    if rta.query("*OPC?") != 1:
        time.sleep(0.1)

fig , real = plt.subplots()
real.semilogx(f, vpp )
real.grid(True)
real.set_xlabel("Frecuencia (Hz)")
real.set_ylabel("Ganancia (V)")
#plt.figure(figsize=(3, 7))
plt.show()

rta.close()
arbGen.close()