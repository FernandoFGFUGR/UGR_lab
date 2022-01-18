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

def acquisition(queue, entries, path):

    valuep = []
    repeat = 0

    if os.path.isfile(path + '.txt'):
        os.remove(path + '.txt') 

    if os.path.isfile(path + '.png'):
        os.remove(path + '.png')

    #Abrir sesion VISA
    rm = pyvisa.ResourceManager()

    rta = rm.open_resource('TCPIP::192.168.100.101::INSTR')
    rta.write("MEASurement1:TIMeout:AUTO")
    rta.write("SYSTem:COMMunicate:INTerface:ETHernet:TRANsfer FD100")
    rta.write("FORM BIN")

    start_time = time.time()

    for i in range(entries):

        if rta.query("*OPC?"):
            p1=float(rta.query("CURSor1:Y1Position?"))
        if rta.query("*OPC?"):
            p2=float(rta.query("CURSor1:Y2Position?"))

        r=(p1-p2)
        #if r != repeat:
            #repeat = r
        valuep.append(r)
        a = np.array(valuep)
        #else:
            #a = np.array(valuep)

        print(str(round(len(valuep)/entries*100, 3))+"%")

        queue.put(a)

        #Escritura fichero CSV
        if len(valuep) == entries:
            auxLen = np.arange(0 , len(valuep) , 1)
            with open(path + '.txt', 'w') as f:
                f.write(str("Time: " + str(round((time.time() - start_time)/60, 3)) + " min\n"))
                for i in auxLen:
                    f.write(str(valuep[i]))
                    f.write('\n')
            lines_seen = set() # holds lines already seen
            with open(path + '.txt', "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i not in lines_seen:
                        f.write(i)
                        lines_seen.add(i)
                f.truncate()

            with open(path + '.txt', "r") as txt_file:
                new_data = list(set(txt_file))
                
            queue.put(a)
            try:
                plt.savefig(path + '.png')
                rta.close() 
                os._exit(1)
            except:
                rta.close() 
                os._exit(1)


def histogram(queue):

    warnings.filterwarnings("ignore")

    def animate(i):

        message = queue.get()
        
        plt.cla()
        plt.ylabel("Entries")
        #plt.yscale('log')
        hist, bin_edges = np.histogram(message, 300)
        bin_edges = bin_edges[1:]
        plt.plot(bin_edges, hist) 

    ani = FuncAnimation(plt.gcf(), animate, interval=100)
    plt.show()
    plt.tight_layout()

if __name__ == "__main__":

    print('Introduce nombre: ')
    name=input() 
    print('Introduce entradas: ')
    entries=int(input())

    path='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/'+name

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
       
