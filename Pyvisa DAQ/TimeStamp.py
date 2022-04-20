import pyvisa
import lab_module as lm

print('Input file name: ')
name=input()+"_timeStamp"

#No tocar/Configuracion
rta = None
try:
	rm = pyvisa.ResourceManager()
	rta = rm.open_resource('TCPIP::192.168.100.101::INSTR')
except Exception as ex:
	print('Error initializing the instrument session:\n' + ex.args[0])
	exit()

#Elimina timeout 
del rta.timeout

rta.write('EXPort:ATABle:NAME "/USB_FRONT/'+name+'.txt"')
while not rta.query("*OPC?"):
    lm.sleep()
print("FIN")   
rta.write("EXPort:ATABle:SAVE")
     
rta.close()
lm.beep()