#Librerias
import numpy as np
import lab_module as lm
import dictionary_SCPI as ds

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
path=lm.path("Curve_IV")
lm.create_dir(path)
path=path + name + named

#No tocar/Configuracion
smu=lm.init_pyvisa(lm.return_instr("smu"))

lm.delete_dir(path + '.txt')

#Reset
smu.write(ds.rst)
#Configuration staircase sweep measure
smu.write(ds.voltMode)
smu.write(ds.sweepMode)
smu.write(ds.sweepSing)
smu.write(ds.sweepLin)
smu.write(":SOUR:VOLT:STAR "+str(vStart))
smu.write(":SOUR:VOLT:STOP "+str(vStop))
points=int(abs(int(vStart)-int(vStop))/sStep)
smu.write(":SOUR:VOLT:POIN "+str(points))

#Set auto-range current measurement
smu.write(ds.smuAuto1)
smu.write(ds.smuAuto2)
smu.write(ds.smuAuto3)

count=0

for j in range(1):

    print('Pulse intro para comenzar prueba ' + str(j+1) + ': ')
    input()

    #Generate triggers by automatic internal algorithm
    smu.write(ds.smuTrig)
    smu.write(":trig:coun "+str(points))

    #Turn on output switch
    smu.write(ds.smuOn)

    #Initiate transition and acquire
    smu.write(ds.smuInit)
    while not smu.query(ds.rdy):
        lm.sleep()
    #Retrieve measurement result
    iResult=smu.query(ds.queryCurr)
    iValues=iResult.split(",")
    iValues[-1]=iValues[-1].rstrip('\n')
    vResult=smu.query(ds.queryVolt)
    vValues=vResult.split(",")
    vValues[-1]=vValues[-1].rstrip('\n')

    smu.write(ds.smuOff)

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

    lm.file_writer_iv(vValues, iValues)
    '''listAux = np.arange(0 , len(vValues) , 1)

    #Escritura fichero
    with open(path + '.txt', 'a+') as f:
        for i in listAux:
            f.write(str(iValues[i]))
            f.write(' ')
            f.write(str(vValues[i]))
            f.write('\n')

    with open(path + '.txt', 'a+') as f:
        f.write('0 0\n')  ''' 

    #Print de control
    print("Prueba " + str(j+1) + " de 6 finalizada.")

smu.close()
lm.beep()