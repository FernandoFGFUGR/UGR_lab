import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter
from numpy.core.fromnumeric import repeat
from numpy.core.shape_base import block
import pyvisa
import os
from matplotlib.pyplot import  figure, step
from scipy.signal import find_peaks
import queue
import threading
from matplotlib.animation import FuncAnimation
import warnings
from datetime import date
import errno

#Funcion de adquisicion
def acquisition(queue, entries, path, ):

    valuep = []
    repeat = 0

    #Supervisa que no existe, si no elimina el anterior
    if os.path.isfile(path + '.txt'):
        os.remove(path + '.txt') 
    if os.path.isfile(path + '.png'):
        os.remove(path + '.png')

    #No tocar/Configuracion
    rm = pyvisa.ResourceManager()
    #Revisar IP en el osciloscopio, puede cambiar
    rta = rm.open_resource('TCPIP::192.168.100.100::INSTR')
    rta.write("MEASurement1:TIMeout:AUTO")
    rta.write("SYSTem:COMMunicate:INTerface:ETHernet:TRANsfer FD100")
    rta.write("FORM BIN")

    #Bucle de las entradas seleccionadas
    while len(valuep) <= entries:

        if rta.query("*OPC?"):
            p1=float(rta.query("CURSor1:Y1Position?"))
        if rta.query("*OPC?"):
            p2=float(rta.query("CURSor1:Y2Position?"))

        r=(p1-p2)
        
        #Comprueba que no sea un valor repetido
        if r != repeat: #and r > -0.25e-8 and r < 1e-8:
            repeat = r
            valuep.append(r)
            a = np.array(valuep)
            queue.put(a)

        #Print de control
        print(str(round(len(valuep)/entries*100, 3))+"%")

        #Creacion de txt
        if len(valuep) == entries:
            auxLen = np.arange(0 , len(valuep) , 1)
            with open(path + '.txt', 'w') as f:
                f.write(str(min(valuep)) + ' ' + str(max(valuep)) + '\n')
                for i in auxLen:
                    f.write(str(valuep[i]))
                    f.write('\n')

        #Cierre seguro + print de la imagen si se ha mantenido
            try:
                plt.savefig(path + '.png')
                rta.close() 
                os._exit(1)
            except:
                rta.close() 
                os._exit(1)

#Funcion de visualizacion
def histogram(queue):

    #Evitar warnings
    warnings.filterwarnings("ignore")

    def animate(i):

        message = queue.get()
        
        plt.cla()
        plt.ylabel("Entries")
        plt.yscale('log')
        hist, bin_edges = np.histogram(message, 250)
        bin_edges = bin_edges[1:] 
        plt.plot(bin_edges, hist) 

    ani = FuncAnimation(plt.gcf(), animate, interval=1)
    plt.show()
    plt.tight_layout()

#Main: nombre/entradas/path/inicializacion/queue
if __name__ == "__main__":

    print('Introduce nombre: ')
    name=input() 
    print('Introduce entradas: ')
    entries=int(input())

    #Creacion de directorios por fechas y nombres
    path='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/Charge_hist/'+str(date.today())+"/"
    try:
        os.mkdir(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    path='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/Charge_hist/'+str(date.today())+"/" + name

    #Inicializamos colar y arrancamos los hilos
    q = queue.Queue()
    acquire = threading.Thread(target=acquisition, args=(q, entries, path, )) 
    acquire.setDaemon(True)
    hist = threading.Thread(target=histogram, args=(q, )) 
    hist.setDaemon(True)
    acquire.start()    
    hist.start()
    acquire.join()
    hist.join()
    q.join()
       
