import lab_module as lm
import dictionary_SCPI as ds

print('Input code name: ')
name=input()
#print('Input vStart: ')
#vStart=float(input())
#print('Input vStop: ')
#vStop=float(input())
print('Inverse o direct(i/d):')
named=input()
while named != "i" and named != "d":
    print("Valor incorrecto, introduce de nuevo \n")
    print('Inverse o direct(i/d):')
    named=input()

if named == "i":
    named="_inverse"
    sStep=0.05
    vStart=-0
    vStop=-45
else:
    named="_direct"
    sStep=0.01
    vStart=0
    vStop=5

#Creacion de directorios por fechas y nombres
path=lm.path("Curve_IV")
lm.create_dir(path)
path=path + name + named

#No tocar/Configuracion
smu=lm.init_pyvisa("smu")

del smu.timeout

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

for j in range(6):

    print('Pulse intro para comenzar prueba ' + str(j+1) + ': ')
    input()

    #Generate triggers by automatic internal algorithm
    smu.write(ds.smuTrig)
    smu.write(":trig:coun "+str(points))

    #Turn on output switch
    smu.write(ds.smuOn)

    #Initiate transition and acquire
    smu.write(ds.smuInit)
    lm.waiting(smu)
    #Retrieve measurement result
    iResult=smu.query(ds.queryCurr)
    iValues=iResult.split(",")
    iValues[-1]=iValues[-1].rstrip('\n')
    vResult=smu.query(ds.queryVolt)
    vValues=vResult.split(",")
    vValues[-1]=vValues[-1].rstrip('\n')

    smu.write(ds.smuOff)

    #Manejo de datos y lectura
    for z in range(len(iValues)):
        if abs(float(iValues[z])) >= 9.9e-03: 
            zaux = z
            #print(zaux)
            break
        else:
            zaux=len(iValues)
    iValues = iValues[:zaux]
    vValues = vValues[:zaux]

    lm.file_writer_iv(vValues, iValues, path)
    #Print de control
    print("Prueba " + str(j+1) + " de 6 finalizada.")

smu.close()
#lm.beep()