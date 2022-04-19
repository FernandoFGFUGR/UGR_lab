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
print('Input triggers: ')
trigg=input()
timeScale=195e-6

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

#No tocar/Configuracion parametros osciloscopio/Solo tocar los 2M de resolucion
timeB=float(rta.query("TIMebase:SCALe?"))
#acqPoints = 2000000*timeB*12 #Parametro a modificar
#print(acqPoints)
#rta.write("ACQuire:POINts " + str(acqPoints))
#rta.write("TIMebase:SCALe " + str(timeScale)) 
rta.write("FORM ASCii")
rta.write("FORM:BORD LSBF")
#rta.write("CHAN"+channel+":DATA:POIN DMAX")
#float(rta.write("CHANnel1:HISTory:TMODe RELative"))
#rta.write("ACQuire:SEGMented:STATe OFF")
#rta.write("ACQuire:NSINgle:COUNt "+trigg)
#rta.write("ACQuire:POINts " + str(acqPoints))

#rta.write("RUNSingle")

#while not rta.query("*OPC?"):
    #time.sleep(5)

for i in range(int(trigg)):
    rta.write("CHAN:HIST:CURR " + str(-int(trigg)+(i+1)))
    #print("CHAN:HIST:CURR" + str(-1*i))
    y_aux=rta.query("CHAN"+channel+":DATA?")

    while not rta.query("*OPC?"):
        time.sleep(0.1)

    y=[float(i) for i in y_aux.split(',')]
    tsr=rta.query("CHAN:HIST:TSR?")
    print(str(round(i/int(trigg)*100))+" %")

    with open(pathF+"_"+str(i)+ ".txt", 'w') as f:
                f.write(str(tsr))
                f.write('\n')
                for i in range(len(y)):
                    f.write(str(round(y[i],5)))
                    f.write('\n')

print("FIN")        
    
#Codigo para calcular el tamano de todos los txt
size = 0
Folderpath = 'Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/Waveform/'+str(date.today())+"/" + name
for path, dirs, files in os.walk(Folderpath):
    for f in files:
        fp = os.path.join(path, f)
        size += os.path.getsize(fp)

#Path de DATA.txt
pathFD= Folderpath + "/DATA.txt"

#Supervisa que no existe, si no elimina el anterior
if os.path.isfile(pathFD):
   os.remove(pathFD)

trigger=float(rta.query("TRIGger:A:LEVel"+channel+"?"))
aRate=float(rta.query("ACQuire:POINts:ARATe?"))
sRate=float(rta.query("ACQuire:SRATe?"))

with open(pathFD, 'w') as f:
    #f.write('Resolucion(ideal): ' + str(acqPoints/(timeScale*12)) + ' Sa/s'+ '\n')  
    #f.write('Num de puntos(ideal): ' + str(2000000*timeScale*12) + '\n')
    f.write('Resolucion(real): ' + str(sRate) + " ! "+ str(aRate) + ' Sa/s'+ '\n')
    f.write('Num de puntos(real): ' + str(len(y)) + '\n')
    f.write('Time base scale: ' + str(timeB) + ' s'+ '\n')  
    #f.write('Time base scale: ' + '41e-6 s'+ '\n')  
    f.write('Trigger (0.5PE): ' +str(trigger)+ ' v' +'\n')
    f.write('Tiempo de ejecucion: ' +str(round(((time.time() - start_time)/60),2))+ ' min' +'\n')  


#Codigo para la creacion del ZIP
zip = zipfile.ZipFile(pathD +"/" + name +'.zip', 'w')
for folder, subfolders, files in os.walk(pathD):
    for file in files:
        if file.endswith('.txt'):
            zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), pathD), compress_type = zipfile.ZIP_DEFLATED) 
zip.close()
rta.close()
for i in range(3):
    winsound.Beep(650-i*100, 500-i*50)