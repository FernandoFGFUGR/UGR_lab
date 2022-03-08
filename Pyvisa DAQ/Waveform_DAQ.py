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
import zipfile
import shutil
import time

print('Input file name: ')
name=input()
print('Input channel: ')
channel=input()

start_time = time.time()

path='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/Waveform/'+str(date.today())+"/"

try:
    os.mkdir(path)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

    #if not os.path.exists(str(date.today())):
        #os.makedirs(str(date.today()))

pathD='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/Waveform/'+str(date.today())+"/" + name 
if os.path.exists(pathD) and os.path.isdir(pathD):
    shutil.rmtree(pathD)

try:
    os.mkdir(pathD)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

pathF='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/Waveform/'+str(date.today())+"/" + name + "/" + name

rta = None
try:
	#Abrir sesion VISA
	rm = pyvisa.ResourceManager()
	rta = rm.open_resource('TCPIP::192.168.100.100::INSTR')
except Exception as ex:
	print('Error initializing the instrument session:\n' + ex.args[0])
	exit()

#Comprobamos que no existen ya esos ficheros
if os.path.isfile(pathF):
   os.remove(pathF) 

x_final = []
y_final = []

num_windows=50

rta.write("ACQuire:POINts 1000000") # // Set points adquisition
rta.write("TIMebase:SCALe 100e-3") # // Set scale to 50 us
acqPoints=float(rta.query("ACQuire:POINts?"))
timeB=float(rta.query("TIMebase:SCALe?"))
trigger=float(rta.query("TRIGger:A:LEVel"+channel+"?"))
#print(timeB)
rta.write("FORM ASCii") # // Set REAL data format
rta.write("FORM:BORD LSBF") # // Set little endian byte order
rta.write("CHAN"+channel+":DATA:POIN DMAX") # // Set sample range to memory data in displayed time range

#pbar = tqdm(total = num_windows, leave=False)

for i in range(num_windows):
    print(str(round(((i+1)/num_windows*100),2))+"%")
    rta.write("SING") # // Start single acquisition
    if rta.query("*OPC?"):
        x_aux=rta.query("CHAN"+channel+":DATA:HEAD?") # // Read header
    aux=[float(i) for i in x_aux.split(',')]
    x = np.linspace(aux[0],aux[1],int(aux[2]))
    x = x + (i*timeB*12)

    y_aux=rta.query("CHAN"+channel+":DATA?") # // Read channel data
    y=[float(i) for i in y_aux.split(',')]
    #for i in range(len(x)):
        #x_final.append(x[i])
        #y_final.append(y[i])
    
    with open(pathF+"_"+str(i)+ ".txt", 'w') as f:
        #f.write(str(timeB) + ' ' + str(num_windows)+" "+str(trigger)+'\n')
        for i in range(len(x)):
            f.write(str(x[i]))
            f.write(' ')
            f.write(str(y[i]))
            f.write('\n')

    #pbar.update(1)

# assign size
size = 0
 
# assign folder path
Folderpath = 'Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/Waveform/'+str(date.today())+"/" + name
 
# get size
for path, dirs, files in os.walk(Folderpath):
    for f in files:
        fp = os.path.join(path, f)
        size += os.path.getsize(fp)

pathFD= Folderpath + "/DATA.txt"

if os.path.isfile(pathFD):
   os.remove(pathFD)

with open(pathFD, 'w') as f:
    f.write('Puntos de adquisicion (resolucion): ' + str(acqPoints/100000) + ' kSa/s'+ '\n')  
    f.write('Tamano ventana: ' + str(round((timeB*12),2)) + ' s' + '\n')   
    f.write('Numero de ventanas: ' + str(num_windows)+'\n') 
    f.write('Tiempo total: ' + str(num_windows*timeB*12)+ ' s' +'\n') 
    f.write('Trigger (0.5PE): ' +str(trigger)+ ' v' +'\n') 
    f.write('Tiempo de ejecucion: ' +str(round(((time.time() - start_time)/60),2))+ ' min' +'\n') 
    f.write('Tamano del fichero: ' + str(round((size / (1024 * 1024)),2)) + ' MB' +'\n')

zip = zipfile.ZipFile(pathD +"/" + name +'.zip', 'w')
 
for folder, subfolders, files in os.walk(pathD):
 
    for file in files:
        if file.endswith('.txt'):
            zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), pathD), compress_type = zipfile.ZIP_DEFLATED)
 
zip.close()

#pbar.close()

#print(len(x_final))

#with open(path, 'w') as f:
    #f.write(str(timeB) + ' ' + str(num_windows)+" "+str(trigger)+'\n')
    #for i in range(len(x_final)):
        #f.write(str(x_final[i]))
        #f.write(' ')
        #f.write(str(y_final[i]))
        #f.write('\n')

#plt.figure(figsize=(12, 4))
#plt.grid(True)
#plt.plot(x_final,y_final) 
#plt.xlabel("S")
#plt.ylabel("V")
#plt.show()


