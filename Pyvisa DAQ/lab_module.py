import errno
import shutil
import os
from RsInstrument import * 
import zipfile
import winsound
from datetime import date
import time
import pyvisa
import dictionary_SCPI as ds
import numpy as np

#Func return de path output
def path(file):
    pathOUT='Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/'+ file + "/" + str(date.today())+"/"
    return pathOUT

#Func para la creacion de directorios
def create_dir(path):
    try:
        os.mkdir(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

#Func para borrar directorio si existe
def delete_dir(path):
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)  

#Func para la creacion del ZIP
def create_zip(path, name):
    zip = zipfile.ZipFile(path +"/" + name +'.zip', 'w')
    for folder, subfolders, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), path), compress_type = zipfile.ZIP_DEFLATED) 
    zip.close()

#Func alarma cuando acaba
def beep():
    for i in range(3):
        winsound.Beep(650-i*100, 500-i*50)

#Func contador en porcentaje
def counter_finish(i, finish):
    print(str(round(i/int(finish)*100, 3))+" %")

#Func creacion fichero data (waveform)
def create_data(path, rta, startTime, len):

    trigger=float(rta.query(ds.lvlTrigger))
    aRate=float(rta.query(ds.arate))
    sRate=float(rta.query(ds.srate))
    timeB=float(rta.query(ds.timeBase))

    with open(path, 'w') as f:
        f.write('Resolucion(real): ' + str(sRate) + " ! "+ str(aRate) + ' Sa/s'+ '\n')
        f.write('Num de puntos(real): ' + str(len) + '\n')
        f.write('Time base scale: ' + str(timeB) + ' s'+ '\n')  
        f.write('Trigger (0.5PE): ' +str(trigger)+ ' v' +'\n')
        f.write('Tiempo de ejecucion: ' +str(round(((currentTime() - startTime)/60),2))+ ' min' +'\n')

#Func generacion de ficheros (waveform)
def file_writer_wf(path, tsr, y, i):
    with open(path+"_"+str(i)+ ".txt", 'w') as f:
                f.write(str(tsr))
                f.write('\n')
                for i in range(len(y)):
                    f.write(str(round(y[i],5)))
                    f.write('\n')

#Func current time
def currentTime():
    return time.time()

#Func sleep
def waiting(rta):
    while not rta.query(ds.rdy):
        time.sleep(0.1)

#Func return instr segun dispositivo
def return_instr(instr):
    if instr == "scope":
        return 'TCPIP::192.168.100.101::INSTR'
    if instr == "smu":
        return 'TCPIP::192.168.100.102::INSTR'
    if instr == "arbGen":
        return 'TCPIP::192.168.100.103::INSTR'

def init_pyvisa(instr):
    rm = pyvisa.ResourceManager()
    rta = rm.open_resource(instr)
    return rta

def file_writer_iv(vValues, iValues):
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
