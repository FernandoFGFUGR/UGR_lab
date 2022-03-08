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
path='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/IV_inverse/'+str(date.today())+"/"

try:
    os.mkdir(path)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

    #if not os.path.exists(str(date.today())):
        #os.makedirs(str(date.today()))

path='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/IV_inverse/'+str(date.today())+"/" + name

#Hacemos un listado de los puertos disponibles
rm = pyvisa.ResourceManager('@py')
rm.list_resources()

#Agregamos cada dispositivo al puerto donde esten conectados, Port1=ASRL5::INSTR, Port2=ASRL6::INSTR, Port3=ASRL7::INSTR, Port4=ASRL8::INSTR,
keithleyE = rm.open_resource('ASRL5::INSTR')
ttiSupply = rm.open_resource('ASRL7::INSTR')
#board = pyfirmata.Arduino('COM11')

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

ttiSupply.write('DELTAV1 0.05')

#Comprobamos que no existen ya esos ficheros
if os.path.isfile(path + '_inverse.txt'):
   os.remove(path + '_inverse.txt')

pbar = tqdm(total = ntest)

#Pausa para iniciar
print('\n')
#print('Pulse intro para comenzar prueba: ')
#input()

for i in range(ntest):

    ttiSupply.write('OP1 0')
    #Pausa para iniciar
    print('\n')
    print('Pulse intro para comenzar prueba ' + str(i+1) + ' : ')

    input()
    ttiSupply.write('OP1 1')

    #Comandos para inicializar power supply QL355P, no hemos conseguido leer datos
    vstart=30
    ttiSupply.write('V1 '+str(vstart))

    time.sleep(1)

    #Adquisicion de datos modificada, ahora se incrementa hasta llegar a 10mA
    inc=0.05
    lenAux=0
    voltList = [vstart]
    ampList = [0] 
    read=keithleyE.query_ascii_values('READ?', container=np.array)
    ampList[0] = round(read[0]*1000, 7)

    #pbar = tqdm(total = 41)

    while voltList[-1] <vstart+13 and read[0]*1000 > -9:

        voltList.append(vstart+inc)
        ttiSupply.write('INCV1')
        read=keithleyE.query_ascii_values('READ?', container=np.array)
        ampList.append(round(read[0]*1000, 7))
        inc+=0.05
        lenAux+=1
        #pbar.update(1)
    ttiSupply.write('OP1 0')

    listAux = np.arange(0 , lenAux , 1) 

    #Escritura fichero TXT
    with open(path + '_inverse.txt', 'a+') as f:
        #f.write('I;V\n')
        for j in listAux:
            f.write(str(i))
            f.write(' ')
            f.write(str(ampList[j]))
            f.write(' ')
            f.write(str(voltList[j]))
            f.write('\n')
        
    pbar.update(1)
ttiSupply.write('OP1 0')
with open(path + '_inverse.txt', 'a+') as f:
    f.write('0 0 0')
#board.digital[7].write(1)

#Calculamos derivada de intensidad, dividimos I'/I y buscamos el maximo.
#dydx = np.diff(ampList) / np.diff(voltList)
#dydx_over_y = dydx/ampList[1:]
#result = (np.where(dydx_over_y == np.amax(dydx_over_y)))

#Hacemos plot de los resultados
#plt.plot(voltList[result[0][0]], ampList[result[0][0]], 'ro')
#plt.plot(voltList, ampList)
#plt.xlabel("Volts")
#plt.ylabel("mAmperes")
#plt.title("Vbr: " + str(voltList[result[0][0]]))
#plt.plot(voltList[1:], dydx_over_y)
#if os.path.isfile(path + '_inverse.png'):
   #os.remove(path + '_inverse.png')   
#plt.savefig(path + '_inverse.png')
#plt.show()

keithleyE.close()
ttiSupply.close()