#Import librerias, algunas pueden estar sin usar
import pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import date
import errno
from tqdm import tqdm
import pyfirmata

#Introducimos el code name
print('Input code name: ')
name=input()

#Introducimos numero de pruebas
#print('Input numero de pruebas: ')
#ntest=int(input())
ntest=6

#Path directorio
path='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/IV_direct/'+str(date.today())+"/"

try:
    os.mkdir(path)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

    #if not os.path.exists(str(date.today())):
        #os.makedirs(str(date.today()))

path='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/IV_direct/'+str(date.today())+"/" + name

#Hacemos un listado de los puertos disponibles
rm = pyvisa.ResourceManager('@py')
rm.list_resources()

#Agregamos cada dispositivo al puerto donde esten conectados, Port1=ASRL5::INSTR, Port2=ASRL6::INSTR, Port3=ASRL7::INSTR, Port4=ASRL8::INSTR,
keithleyE = rm.open_resource('ASRL5::INSTR')
ttiSupply = rm.open_resource('ASRL7::INSTR')
board = pyfirmata.Arduino('COM9')

#Ajustes de comunicacion
keithleyE.read_termination = '\n'
keithleyE.write_termination = '\n'
del keithleyE.timeout
keithleyE.baud_rate=9600

#Comandos SCPI para inicializar Keithley Electrometro
keithleyE.write("*RST")
keithleyE.write("SYST:ZCH ON")
keithleyE.write("FUNC 'CURR'")
keithleyE.write("CURR:RANG  20e-12")
keithleyE.write("SYST:ZCOR ON")
keithleyE.write("CURR:RANG:AUTO ON")
keithleyE.write("SYST:ZCH OFF")

ttiSupply.write('DELTAV1 0.01')

#Comprobamos que no existen ya esos ficheros
if os.path.isfile(path + '_direct.txt'):
   os.remove(path + '_direct.txt') 

pbar = tqdm(total = ntest)

for i in range(ntest):

    #Seleccionamos canal
    temp = '{0:04b}'.format(i)
    board.digital[2].write(int(temp[0]))
    board.digital[3].write(int(temp[1]))
    board.digital[4].write(int(temp[2]))
    board.digital[5].write(int(temp[3]))

    print("Comenzando prueba SiPM: "+str(i+1))

    #Comandos de la power supply QL355P, no hemos conseguido leer datos
    vstart=0
    ttiSupply.write('V1 '+str(vstart))

    #Tiempo para que la fuente de alimentacion alcance el voltaje pedido.

    ttiSupply.write('OP1 1')
    board.digital[6].write(0)

    time.sleep(1)

    #Adquisicion de datos modificada, ahora se incrementa hasta llegar a 10mA
    inc=0.01
    lenAux=0
    voltList = [vstart]
    ampList = [0] 
    read=keithleyE.query_ascii_values('READ?', container=np.array) 
    ampList[0] = round(read[0]*1000, 7)

    while voltList[-1] <vstart+20 and read[0]*1000 < 9:
        voltList.append(vstart + inc)
        ttiSupply.write('INCV1')
        read=keithleyE.query_ascii_values('READ?', container=np.array)
        ampList.append(round(read[0]*1000, 7))
        inc+=0.01
        lenAux+=1
    ttiSupply.write('OP1 0')
    listAux = np.arange(0 , lenAux , 1)
    #Buscamos dos puntos para hacer la recta, 1 entre 2-3mA y otro entre 8-9mA
    #for j in listAux:
        #if 1 < ampList[j] < 2:
            #p1=j
        #if 8 < ampList[j] < 9:
            #p2=j

    #Calculamos QR
    #m=(ampList[p2]-ampList[p1])/(voltList[p2]-voltList[p1])
    #QR=round(1/m*1000, 5)
    #print('QR =', QR, 'Ohms')

    #Escritura fichero TXT
    with open(path + '_direct.txt', 'a+') as f:
        #f.write('Current;Volts\n')
        for j in listAux:
            f.write(str(i))
            f.write(' ')
            f.write(str(ampList[j]))
            f.write(' ')
            f.write(str(voltList[j]))
            f.write('\n')
    pbar.update(1)

ttiSupply.write('OP1 0')
board.digital[6].write(1)

#Hacemos plot de los resultados
#plt.plot(voltList, ampList)
#plt.plot(voltList[p1], ampList[p1], 'ro')
#plt.plot(voltList[p2], ampList[p2],  'ro')
#plt.title("QR= "+str(QR))
#plt.xlabel("Volts")
#plt.ylabel("mAmperes")
#if os.path.isfile(path + '_direct.png'):
   #os.remove(path + '_direct.png') 
#plt.savefig(path + '_direct.png')
#plt.show()

keithleyE.close()
ttiSupply.close()