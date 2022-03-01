#librerias
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter
import pyvisa
import os
from matplotlib.pyplot import  figure, step
from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details
from datetime import date
import errno
from tqdm import tqdm

print('Input file name: ')
name=input()
print('Input channel: ')
channel=input()

path='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/Waveform/'+str(date.today())+"/"

try:
    os.mkdir(path)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

    #if not os.path.exists(str(date.today())):
        #os.makedirs(str(date.today()))

path='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/Waveform/'+str(date.today())+"/" + name + ".txt"

rta = None
try:
	#Abrir sesion VISA
	rm = pyvisa.ResourceManager()
	rta = rm.open_resource('TCPIP::192.168.100.101::INSTR')
except Exception as ex:
	print('Error initializing the instrument session:\n' + ex.args[0])
	exit()

#Comprobamos que no existen ya esos ficheros
if os.path.isfile(path):
   os.remove(path) 

x_final = []
y_final = []

num_windows=10

rta.write("ACQuire:POINts 500000") # // Set points adquisition
rta.write("TIMebase:SCALe 100e-3") # // Set scale to 50 us
timeB=float(rta.query("TIMebase:SCALe?"))
trigger=float(rta.query("TRIGger:A:LEVel"+channel+"?"))
#print(timeB)
rta.write("FORM ASCii") # // Set REAL data format
rta.write("FORM:BORD LSBF") # // Set little endian byte order
rta.write("CHAN"+channel+":DATA:POIN DMAX") # // Set sample range to memory data in displayed time range

pbar = tqdm(total = num_windows, leave=False)

for i in range(num_windows):
    rta.write("SING") # // Start single acquisition
    if rta.query("*OPC?"):
        x_aux=rta.query("CHAN"+channel+":DATA:HEAD?") # // Read header
    aux=[float(i) for i in x_aux.split(',')]
    x = np.linspace(aux[0],aux[1],int(aux[2]))
    x = x + (i*timeB*12)

    y_aux=rta.query("CHAN"+channel+":DATA?") # // Read channel data
    y=[float(i) for i in y_aux.split(',')]
    for i in range(len(x)):
        x_final.append(x[i])
        y_final.append(y[i])
    pbar.update(1)
pbar.close()

print(len(x))

with open(path, 'w') as f:
    f.write(str(timeB*12*num_windows)+" "+str(trigger)+'\n')
    for i in range(len(x_final)):
        f.write(str(x_final[i]))
        f.write(' ')
        f.write(str(y_final[i]))
        f.write('\n')

plt.figure(figsize=(12, 4))
plt.grid(True)
plt.plot(x_final,y_final) 
plt.xlabel("S")
plt.ylabel("V")
plt.show()


