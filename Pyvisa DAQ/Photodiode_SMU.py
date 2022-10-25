import lab_module as lm
import dictionary_SCPI as ds
from datetime import date

#Lectura de parametros
print('Input code name: ')
name=input()
'''print('Working voltage: ')
vol=input()
print('Measuremente time: ')
tiempo=input()'''

#Creacion de directorios por fechas y nombres
path='/Users/alejandrosanchez/software/pyvisa/output/'+str(date.today())+"/"
lm.create_dir(path)
path=path + name 

#No tocar/Configuracion
smu=lm.init_pyvisa("smu")
del smu.timeout
lm.delete_dir(path + '.txt')

#Reset
smu.write(ds.rst)
#Configuration
#smu.write(":SOUR:FUNC:TRIG:CONT 3")
smu.write(":SENS:CURR:PROT 0.01")
smu.write(":SOUR:FUNC:MODE VOLT")
smu.write(":SOUR:VOLT 1.4")
#smu.write(":SOUR:FUNC:MODE FIX")
#smu.write(ds.smuOn)
#smu.write(":SOUR:VOLT:TRIG 1")

#lm.chronometter(lm.currentTime(),0.1)
#smu.write(ds.smuInit)
#smu.write(ds.smuTrig)

#result=smu.query(ds.queryCurr)
#result=smu.query(":meas:curr? (@1)")
#print(result)
'''result=smu.query(ds.queryCurr)
print(result)
result=smu.query(ds.queryCurr)
print(result)'''
#smu.write(ds.smuOff)
count=0

I=[]
startTime=lm.currentTime()
while(lm.currentTime()-startTime) < 2400:
    result=smu.query(":meas:curr? (@1)")
    I.append(result)
    #print(result)
    lm.time.sleep(1)
    count+=1

f=open(path+'_direct.txt','w')
for i in range(len(I)):
    f.write(I[i])

f.close()


print(count)   
smu.close()
