#Librerias
import pyvisa
import time
import numpy as np
import os
from datetime import date
import errno

print('Input code name: ')
name=input()

#print('Input numero de pruebas: ')
#ntest=int(input())
ntest=2

#Creacion de directorios por fechas y nombres
path='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/Curve_IV/'+str(date.today())+"/"
try:
    os.mkdir(path)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
path='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/Curve_IV/'+str(date.today())+"/" + name

#No tocar/Configuracion
rm = pyvisa.ResourceManager('@py')
rm.list_resources()
#Revisar puertos, puede cambiar
keithleyE = rm.open_resource('ASRL3::INSTR')
ttiSupply = rm.open_resource('ASRL5::INSTR')
keithleyE.read_termination = '\n'
keithleyE.write_termination = '\n'
del keithleyE.timeout
keithleyE.baud_rate=9600
keithleyE.write("*RST")
keithleyE.write("SYST:ZCH ON")
keithleyE.write("FUNC 'CURR'")
keithleyE.write("CURR:RANG  20e-12")
keithleyE.write("SYST:ZCOR ON")
keithleyE.write("CURR:RANG:AUTO ON")
keithleyE.write("SYST:ZCH OFF")

#Avance de los pasos del barrido
ttiSupply.write('DELTAV1 0.01')

#Supervisa que no existe, si no elimina el anterior
if os.path.isfile(path + '_direct.txt'):
   os.remove(path + '_direct.txt') 

#Comienzo de las pruebas/Bucle de ntest
for i in range(ntest):

    #Comando para apagar la power supply
    ttiSupply.write('OP1 0')

    print('Pulse intro para comenzar prueba ' + str(i+1) + ' : ')
    input()

    #Comando para encender la power supply
    ttiSupply.write('OP1 1')

    #Voltaje en el que comienza el barrido
    vstart=0
    ttiSupply.write('V1 '+str(vstart))
    time.sleep(2)

    #Configuracion variables para el barrido
    inc=0.01
    lenAux=0
    voltList = [0]
    ampList = [0] 
    read=keithleyE.query_ascii_values('READ?', container=np.array) 
    ampList[0] = round(read[0]*1000, 7)

    #Barrido por pasos hasta llegar a un overvoltage o 9mA
    while voltList[-1] <vstart+5 and read[0]*1000 < 9:
        voltList.append(0 + inc)
        ttiSupply.write('INCV1')
        read=keithleyE.query_ascii_values('READ?', container=np.array)
        ampList.append(round(read[0]*1000, 7))
        inc+=0.01
        lenAux+=1

    listAux = np.arange(0 , lenAux , 1)

    #Se anade la medicion altual al mismo fichero
    with open(path + '_direct.txt', 'a+') as f:
        for j in listAux:
            f.write(str(i))
            f.write(' ')
            f.write(str(ampList[j]))
            f.write(' ')
            f.write(str(voltList[j]))
            f.write('\n')

    #Print de control
    print("Prueba " + str(i+1) + " de " + str(ntest) + " finalizada.")

#Comando para apagar la power supply al finalizar
ttiSupply.write('OP1 0')

#Anadimos zeros al final para facilitar la lectura en ROOT
with open(path + '_direct.txt', 'a+') as f:
    f.write('0 0 0')

#Cerramos sesion
keithleyE.close()
ttiSupply.close()