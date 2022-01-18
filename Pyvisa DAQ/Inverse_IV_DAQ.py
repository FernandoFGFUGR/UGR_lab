#Import librerias, algunas pueden estar sin usar
import pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt
import os

#Introducimos el code name
print('Input code name: ')
name=input()

#Introducimos numero de pruebas
print('Input numero de pruebas: ')
ntest=int(input())

#Path directorio
path='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/'

#Hacemos un listado de los puertos disponibles
rm = pyvisa.ResourceManager('@py')
rm.list_resources()

#Agregamos cada dispositivo al puerto donde esten conectados, Port1=ASRL5::INSTR, Port2=ASRL6::INSTR, Port3=ASRL7::INSTR, Port4=ASRL8::INSTR,
keithleyE = rm.open_resource('ASRL5::INSTR')
ttiSupply = rm.open_resource('ASRL7::INSTR')

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
if os.path.isfile(path + name + 'inverse.txt'):
   os.remove(path + name + 'inverse.txt')

for i in range(ntest):

    #Pausa para iniciar
    print('Pulse intro para empezar prueba ' + str(i+1) + ' : ')
    ntest=input()

    #Comandos de la power supply QL355P, no hemos conseguido leer datos
    ttiSupply.write('V1 31')

    #Tiempo para que la fuente de alimentacion alcance el voltaje pedido.
    time.sleep(2)

    #Adquisicion de datos modificada, ahora se incrementa hasta llegar a 10mA
    inc=0.05
    lenAux=0
    voltList = [30]
    ampList = [0] 
    read=keithleyE.query_ascii_values('READ?', container=np.array)
    ampList[0] = round(read[0]*1000, 7)

    while read[0]*1000 > -2:
        voltList.append(30+inc)
        ttiSupply.write('INCV1')
        read=keithleyE.query_ascii_values('READ?', container=np.array)
        ampList.append(round(read[0]*1000, 7))
        inc+=0.05
        lenAux+=1

    listAux = np.arange(0 , lenAux , 1) 

    #Escritura fichero TXT
    with open(path + name + '_set_data_inverse.txt', 'a+') as f:
        #f.write('I;V\n')
        for j in listAux:
            f.write(str(i))
            f.write(' ')
            f.write(str(ampList[j]))
            f.write(' ')
            f.write(str(voltList[j]))
            f.write('\n')

#Calculamos derivada de intensidad, dividimos I'/I y buscamos el maximo.
dydx = np.diff(ampList) / np.diff(voltList)
dydx_over_y = dydx/ampList[1:]
result = (np.where(dydx_over_y == np.amax(dydx_over_y)))

#Hacemos plot de los resultados
plt.plot(voltList[result[0][0]], ampList[result[0][0]], 'ro')
plt.plot(voltList, ampList)
plt.xlabel("Volts")
plt.ylabel("mAmperes")
plt.title("Vbr: " + str(voltList[result[0][0]]))
plt.plot(voltList[1:], dydx_over_y)
if os.path.isfile(path + name + '_set_plot_inverse.png'):
   os.remove(path + name + '_set_plot_inverse.png')   
plt.savefig(path + name + '_set_plot_inverse.png')
plt.show()

keithleyE.close()
ttiSupply.close()