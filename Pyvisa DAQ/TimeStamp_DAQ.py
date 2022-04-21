import pyvisa
import lab_module as lm
import dictionary_SCPI as ds

print('Input file name: ')
name=input()+"_timeStamp"

#No tocar/Configuracion
rta = None
try:
	rta=lm.init_pyvisa(lm.return_instr("scope"))
except Exception as ex:
	print('Error initializing the instrument session:\n' + ex.args[0])
	exit()

#Elimina timeout 
del rta.timeout

rta.write('EXPort:ATABle:NAME "/USB_FRONT/'+name+'.txt"')
while not rta.query(ds.rdy):
    lm.sleep()
print("FIN")   
rta.write(ds.saveTS)
     
rta.close()
lm.beep()