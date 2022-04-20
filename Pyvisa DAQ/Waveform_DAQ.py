import pyvisa
import lab_module as lm

print('Input file name: ')
name=input()
print('Input channel: ')
channel=input()

start_time = lm.currentTime()

#Creacion de directorios por fechas y nombres
path=lm.path("Waveform")

lm.create_dir(path)

pathD = path + name 

lm.delete_dir(pathD)

lm.create_dir(pathD)

pathF = pathD + "/" + name

lm.delete_dir(pathF)

#No tocar/Configuracion
rta = None
instr=lm.return_instr("scope")

try:
	rm = pyvisa.ResourceManager()
	rta = rm.open_resource(instr)
except Exception as ex:
	print('Error initializing the instrument session:\n' + ex.args[0])
	exit()

#Elimina timeout 
del rta.timeout

rta.write("FORM ASCii")
rta.write("FORM:BORD LSBF")
trigg=rta.query("ACQ:AVA?")

for i in range(int(trigg)):
    
    rta.write("CHAN:HIST:CURR " + str(-int(trigg)+(i+1)))
    y_aux=rta.query("CHAN"+channel+":DATA?")
    y=[float(i) for i in y_aux.split(',')]

    while not rta.query("*OPC?"):
        lm.sleep()

    tsr=rta.query("CHAN:HIST:TSR?")

    lm.file_writer(pathF, tsr, y, i) 
    lm.counter_finish(i, trigg)      

#Path de DATA.txt
pathFD= pathD + "/DATA.txt"

lm.delete_dir(pathFD)

trigger=float(rta.query("TRIGger:A:LEVel"+channel+"?"))
aRate=float(rta.query("ACQuire:POINts:ARATe?"))
sRate=float(rta.query("ACQuire:SRATe?"))
timeB=float(rta.query("TIMebase:SCALe?"))

lm.create_data(pathFD, sRate, aRate, len(y), timeB, trigger, start_time)

lm.create_zip(pathD, name)

rta.close()

lm.beep()