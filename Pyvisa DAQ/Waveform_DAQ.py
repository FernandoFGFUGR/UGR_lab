import lab_module as lm
import dictionary_SCPI as ds

print('Input file name: ')
name=input()

#Descomentar si hace falta cambiar de canal
channel=str(1)
#print('Input channel: ')
#channel=input()

startTime = lm.currentTime()

lm.chronometter(startTime, 25)

#Creacion de directorios por fechas y nombres
path=lm.path("Waveform")
lm.create_dir(path)
pathD = path + name 
lm.delete_dir(pathD)
lm.create_dir(pathD)
pathF = pathD + "/" + name
lm.delete_dir(pathF)

try:
    #rta=lm.init_pyvisa(lm.return_instr("scope"))
    rta=lm.init_pyvisa("scope")
except Exception as ex:
	print('Error initializing the instrument session:\n' + ex.args[0])
	exit()

rta.write("STOP")

del rta.timeout

rta.write(ds.ascii)
rta.write(ds.lsbf)
trigg=rta.query(ds.numCounts)
#trigg=10
for i in range(int(trigg)):
    
    rta.write(ds.selectCurr(trigg, i))
    y_aux=rta.query(ds.waveform(channel))
    #print(y_aux)
    y=[float(i) for i in y_aux.split(',')]

    lm.waiting(rta)

    tsr=rta.query(ds.tsr)

    lm.file_writer_wf(pathF, tsr, y, i) 
    lm.counter_finish(i, trigg)      

pathFD= pathD + "/DATA.txt"
lm.delete_dir(pathFD)
lm.create_data(pathFD, rta, startTime, len(y))
lm.create_zip(pathD, name)

rta.close()
lm.beep()