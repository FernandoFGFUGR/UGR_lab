#librerias
from asyncio.windows_events import NULL
from curses.ascii import isdigit
import matplotlib.pyplot as plt
import pyvisa
import time
from itertools import count
from matplotlib.animation import FuncAnimation
from matplotlib.pyplot import  figure, step
import os
import numpy as np
from datetime import date
import errno
import shutil
import winsound

#No tocar/Configuracion
rm = pyvisa.ResourceManager()
rta = rm.open_resource('TCPIP::192.168.100.101::INSTR')
rta.write("TIMebase:SCALe 20e-6")

#Variables
index = count()
valuep = []
a = np.array([])
aux = 0

print('Input file name: ')
name=input()
print('Input num trigger: ')
num=input()

start_time = time.time()

#Creacion de directorios por fechas y nombres
path='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/DCR/'+str(date.today())+"/"
try:
    os.mkdir(path)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
pathD='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/DCR/'+str(date.today())+"/" + name

#Supervisa que no existe, si no elimina el anterior
if os.path.exists(pathD) and os.path.isdir(pathD):
    shutil.rmtree(pathD)

#Creacion de subdirectorio
try:
    os.mkdir(pathD)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
pathF='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/DCR/'+str(date.today())+"/" + name + "/" + name

#Supervisa que no existe, si no elimina el anterior
if os.path.isfile(pathF):
   os.remove(pathF) 

del rta.timeout

trigger=float(rta.query("TRIGger:A:LEVel1?"))

#Funcion histograma animado
def animate(i):

    global aux
        
    p1Aux=float(rta.query("TCOunter:RESult:ACTual:FREQuency?"))
    p1=p1Aux #*1000/36
    #Comprobacion resultados repetidos
    if aux != p1 and p1 <1e20:
        valuep.append(p1)
        a = np.array(valuep)
    else:
        a = np.array(valuep)
    aux = p1
    
    plt.cla()
    plt.xlabel("mHz/mm2")
    plt.ylabel("Bins")
    plt.yscale('log')
    #plt.xscale('log')
    plt.hist(a, bins=20, color='c', edgecolor='k', alpha=0.5)
    plt.axvline(a.mean(), color='k', linestyle='dashed', linewidth=1)
    plt.tight_layout()

    TIME=0
    
    #Print de control
    print(str(round((len(valuep)/int(num)*100),2))+"%")

    #Creacion fichero txt
    if len(valuep) == int(num):
        for i in range(len(valuep)):
            TIME+=1/valuep[i]
        with open(pathF+ ".txt" , 'w') as f:
            f.write('Time:' + str(TIME) +"\n")
            f.write('TAM:' + str(len(valuep)) +"\n")
            f.write('Trigger:' + str(trigger) +"\n")
            f.write('DCR((NO)mHz/mm2):' + str(len(valuep)/TIME) +"\n")
            f.write('DCR2((NO)mHz/mm2):' + str(a.mean()) +"\n")
            f.write('Tiempo de ejecucion: ' +str(round(((time.time() - start_time)/60),2))+ ' min' +'\n')
            for i in range(len(valuep)):
                f.write(str(valuep[i]))
                f.write('\n') 
            
        #Cierre seguro + print de la imagen si se ha mantenido
        try: 
            plt.savefig(pathF + '.png')
            rta.close()
            for i in range(3):
                winsound.Beep(650-i*100, 500-i*50)
            os._exit(1)
        except:
            rta.close()
            for i in range(3):
                winsound.Beep(650-i*100, 500-i*50) 
            os._exit(1)

ani = FuncAnimation(plt.gcf(), animate, interval=1)

#No se deberia leer nunca este codigo
plt.tight_layout()
plt.show()
time.sleep(3)
rta.close()
for i in range(3):
    winsound.Beep(650-i*100, 500-i*50)
os._exit(1)

