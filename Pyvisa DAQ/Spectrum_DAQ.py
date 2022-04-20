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
import lab_module as lm

#Funcion de adquisicion
def acquisition(queue, entries, path, ):

    valuep = []
    repeat = 0

    #Supervisa que no existe, si no elimina el anterior
    lm.delete_dir(path+'.txt')
    lm.delete_dir(path+'.png')

    rm = pyvisa.ResourceManager()
    #arbGen = rm.open_resource(lm.return_instr("arbGen"))
    rta = rm.open_resource(lm.return_instr("scope"))
    #arbGen.write("C1:BSWV WVTP,PULSE")
    #arbGen.write("C1:BSWV WIDTH,100e-9")
    #arbGen.write("C1:BSWV FREC,1e3")
    #arbGen.write("C1:OUTP ON")
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
        lm.counter_finish(len(valuep), entries)

        try:
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
                    lm.beep()
                    os._exit(1)
                    
                except:
                    rta.close() 
                    lm.beep()
                    os._exit(1)
        except KeyboardInterrupt:
            auxLen = np.arange(0 , len(valuep) , 1)
            with open(path + '.txt', 'w') as f:
                f.write(str(min(valuep)) + ' ' + str(max(valuep)) + '\n')
                for i in auxLen:
                    f.write(str(valuep[i]))
                    f.write('\n')
            rta.close() 
            lm.beep()
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
    path=lm.path("Charge_hist")
    lm.create_dir(path)
    pathF=path + name

    #Inicializamos colar y arrancamos los hilos
    q = queue.Queue()
    acquire = threading.Thread(target=acquisition, args=(q, entries, pathF, )) 
    acquire.setDaemon(True)
    hist = threading.Thread(target=histogram, args=(q, )) 
    hist.setDaemon(True)
    acquire.start()    
    hist.start()
    acquire.join()
    hist.join()
    q.join()
       
