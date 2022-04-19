#Librerias
import pyvisa
import numpy as np
import os
from datetime import date
import errno
import time

print('Input code name: ')
name=input()
print('Input vStart: ')
vStart=float(input())
print('Input vStop: ')
vStop=float(input())

if vStart >= 0:
    named="_direct"
    sStep=0.01
    if vStart > vStop:
        aux=vStart
        vStart = vStop
        vStop =aux
else:
    named="_inverse"
    sStep=0.05
    if vStart < vStop:
        aux=vStart
        vStart = vStop
        vStop =aux

#Creacion de directorios por fechas y nombres
path='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/Curve_IV/'+str(date.today())+"/"
try:
    os.mkdir(path)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
path='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/Curve_IV/'+str(date.today())+"/" + name + named

#No tocar/Configuracion
rm = pyvisa.ResourceManager('@py')
smu=rm.open_resource('TCPIP::192.168.100.102::INSTR')

#Supervisa que no existe, si no elimina el anterior
if os.path.isfile(path + '.txt'):
   os.remove(path + '.txt') 

#Reset
smu.write("*RST")
#Configuration staircase sweep measure
smu.write(":SOUR:VOLT:MODE VOLT")
smu.write(":SOUR:VOLT:MODE SWE")
smu.write(":SOUR:SWE:STA SING")
smu.write(":SOUR:SWE:SPAC LIN")
smu.write(":SOUR:VOLT:STAR "+str(vStart))
smu.write(":SOUR:VOLT:STOP "+str(vStop))
points=int(abs(int(vStart)-int(vStop))/sStep)
smu.write(":SOUR:VOLT:POIN "+str(points))

#Set auto-range current measurement
smu.write(":sens:func ""curr""")
smu.write(":sens:curr:nplc 0.1")
smu.write(":sens:curr:prot 0.01")

count=0

for j in range(1):

    print('Pulse intro para comenzar prueba ' + str(j+1) + ': ')
    input()

    #Generate triggers by automatic internal algorithm
    smu.write(":trig:sour aint")
    smu.write(":trig:coun "+str(points))

    #Turn on output switch
    smu.write(":outp on")

    #Initiate transition and acquire
    smu.write(":init (@1)")
    while not smu.query("*OPC?"):
        time.sleep(0.1)
    #Retrieve measurement result
    iResult=smu.query(":fetc:arr:curr? (@1)")
    iValues=iResult.split(",")
    iValues[-1]=iValues[-1].rstrip('\n')
    vResult=smu.query(":fetc:arr:volt? (@1)")
    vValues=vResult.split(",")
    vValues[-1]=vValues[-1].rstrip('\n')

    smu.write(":outp off")

    #print(vValues)
    #print(iValues)

    #Manejo de datos y lectura
    for z in range(len(iValues)):
        if abs(float(iValues[z])) >= 9.9e-03: 
            zaux = z
            #print(zaux)
            break
    iValues = iValues[:zaux]
    vValues = vValues[:zaux]
    listAux = np.arange(0 , len(vValues) , 1)

    #Escritura fichero
    with open(path + '.txt', 'a+') as f:
        for i in listAux:
            f.write(str(iValues[i]))
            f.write(' ')
            f.write(str(vValues[i]))
            f.write('\n')

    with open(path + '.txt', 'a+') as f:
        f.write('0 0\n')   

    #Print de control
    print("Prueba " + str(j+1) + " de 6 finalizada.")

smu.close()