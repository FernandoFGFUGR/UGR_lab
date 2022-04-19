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
import winsound

print('Input file name: ')
name=input()
print('Input channel: ')
channel=input()
timeScale=20e-6

start_time = time.time()

#Creacion de directorios por fechas y nombres
path='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/Waveform/'+str(date.today())+"/"
try:
    os.mkdir(path)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
pathD='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/Waveform/'+str(date.today())+"/" + name 

#Supervisa que no existe, si no elimina el anterior
if os.path.exists(pathD) and os.path.isdir(pathD):
    shutil.rmtree(pathD)

#Creacion de subdirectorio
try:
    os.mkdir(pathD)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
pathF='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/Waveform/'+str(date.today())+"/" + name + "/" + name

#No tocar/Configuracion
rta = None
try:
	rm = pyvisa.ResourceManager()
	rta = rm.open_resource('TCPIP::192.168.100.101::INSTR')
except Exception as ex:
	print('Error initializing the instrument session:\n' + ex.args[0])
	exit()

#Supervisa que no existe, si no elimina el anterior
if os.path.isfile(pathF):
   os.remove(pathF) 

#Elimina timeout 
del rta.timeout
num_files=0

#No tocar/Configuracion parametros osciloscopio/Solo tocar los 2M de resolucion
rta.write("TIMebase:SCALe " + str(timeScale)) 
rta.write("FORM ASCii")
rta.write("FORM:BORD LSBF")
rta.write("CHAN"+channel+":DATA:POIN DMAX")
#float(rta.write("CHANnel1:HISTory:TMODe RELative"))
rta.write("ACQuire:SEGMented:STATe ON")
rta.write("ACQuire:NSINgle:COUNt 10")
rta.write("RUNSingle")

while not rta.query("*OPC?"):
    time.sleep(0.1)
rta.write("CHAN:HIST:CURR -5")
hola=rta.query("CHAN:HIST:TSR?")
print(hola)
rta.write("CHAN:HIST:CURR -3")
hola=rta.query("CHAN:HIST:TSR?")
print(hola)
#rta.write('EXPort:ATABle:NAME "/USB_FRONT/'+name+'.txt"')
#while not rta.query("*OPC?"):
    #time.sleep(0.1)
#print("FIN")   
#rta.write("EXPort:ATABle:SAVE")
     

rta.close()
for i in range(3):
    winsound.Beep(650-i*100, 500-i*50)