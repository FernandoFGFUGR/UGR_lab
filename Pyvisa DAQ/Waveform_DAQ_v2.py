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
print('Input size window: ')
timeScale=float(input())/12
print('Input total time: ')
totalW=float(input())/(12*timeScale)

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
num_windows=int(totalW)
rta.write("TIMebase:SCALe " + str(timeScale)) 
acqPointsAux=float(rta.query("ACQuire:POINts?"))
timeB=float(rta.query("TIMebase:SCALe?"))
acqPoints = 2000000*timeB*12 #Parametro a modificar
rta.write("ACQuire:POINts " + str(acqPoints)) 
trigger=float(rta.query("TRIGger:A:LEVel"+channel+"?"))
rta.write("FORM ASCii")
rta.write("FORM:BORD LSBF")
rta.write("CHAN"+channel+":DATA:POIN DMAX")
#rta.write("TRIGger:A:LEVel1 -20e-3")
rta.write("RUNC") #Se puede cambiar por SING/RUNC para mas precision-lento
aRate=float(rta.query("ACQuire:POINts:ARATe?"))
sRate=float(rta.query("ACQuire:SRATe?"))
auxperiod = 0
try:
    #Bucle de la adquisicion
    while num_windows > num_files:
        #print("HOLA")
        #rta.write("SING")
        y_aux=rta.query("CHAN"+channel+":DATA?")
        #print("HOLA1")
        period=float(rta.query("TCOunter:RESult:ACTual:PERiod?"))
        #print("ADIOS")
            
        y=[float(i) for i in y_aux.split(',')]

        if auxperiod != period and period < 1e20:
            #Print de control
            print(str(round(((num_files+1)/num_windows*100),2))+"%")
            
            #Escritura fichero txt
            with open(pathF+"_"+str(num_files)+ ".txt", 'w') as f:
                f.write(str(period))
                f.write('\n')
                for i in range(len(y)):
                    f.write(str(round(y[i],5)))
                    f.write('\n')
            num_files+=1
            auxperiod = period
        

except KeyboardInterrupt:
    pass

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

#Creacion de fichero DATA.txt
with open(pathFD, 'w') as f:
    f.write('Resolucion(ideal): ' + str(acqPoints/(timeScale*12)) + ' Sa/s'+ '\n')  
    f.write('Num de puntos(ideal): ' + str(2000000*timeB*12) + '\n')
    f.write('Resolucion(real): ' + str(sRate) + " ! "+ str(aRate) + ' Sa/s'+ '\n')
    f.write('Num de puntos(real): ' + str(len(y)) + '\n')
    f.write('Tamano ventana: ' + str(round((timeB*12),5)) + ' s' + '\n')   
    f.write('Numero de ventanas(ideal): ' + str(num_windows)+'\n') 
    f.write('Numero de ventanas(real): ' + str(num_files)+'\n') 
    f.write('Tiempo total: ' + str(num_windows*timeB*12)+ ' s' +'\n') 
    f.write('Trigger (0.5PE): ' +str(trigger)+ ' v' +'\n') 
    f.write('Tiempo de ejecucion: ' +str(round(((time.time() - start_time)/60),2))+ ' min' +'\n') 
    f.write('Tamano del fichero: ' + str(round((size / (1024 * 1024)),2)) + ' MB' +'\n')


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