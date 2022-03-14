#librerias
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import seaborn as sns
import pyvisa
import time
from itertools import count
from matplotlib.animation import FuncAnimation
from matplotlib.pyplot import  figure, step
import os
import numpy as np

#Abrir sesion VISA
rm = pyvisa.ResourceManager()
rta = rm.open_resource('TCPIP::192.168.100.100::INSTR')

path='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/'

#n_bins = 50
index = count()
valuep = []
a = np.array([])
aux = 0

def animate(i):
    global aux
        
    p1=float(rta.query("TCOunter:RESult:ACTual:FREQuency?"))
    #print(p1)
    #if p1 > 0:
        #print(p1)
        #valuep.append(p1)
    if aux != p1:
        valuep.append(p1)
        a = np.array(valuep)
    else:
        a = np.array(valuep)
    aux = p1
    

    plt.cla()

    plt.xlabel("Hz")
    plt.ylabel("Bins")
    #plt.yscale('log')

    plt.hist(a, bins=20, color='c', edgecolor='k', alpha=0.65)
    #sns.histplot(data=valuep, element="step", bins=100)
    plt.axvline(a.mean(), color='k', linestyle='dashed', linewidth=1)
    #sns.histplot(data=valuep, bins="auto")
    #sns.histplot(data=valuep, binwidth=1, bins=3000)
    #sns.histplot(data=valuep, element="poly", bins=25)
    #sns.histplot(data=valuep, element="poly")
    #sns.histplot(data=valuep, kde=True, element="step")
    #sns.histplot(data=valuep)

    plt.tight_layout()
    print(round((len(valuep)/1000*100),2))
    if len(valuep) == 1000:
        try:
            plt.savefig(path + '.png')
            rta.close() 
            os._exit(1)
        except:
            rta.close() 
            os._exit(1)


ani = FuncAnimation(plt.gcf(), animate, interval=1)

plt.tight_layout()
plt.show()
time.sleep(3)
rta.close()
exit()

