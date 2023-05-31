import lab_module as lm
import dictionary_SCPI as ds
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import os
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import customtkinter as ctk
from scipy.signal import argrelextrema
from scipy.optimize import curve_fit
from matplotlib import colors
from scipy.signal import find_peaks
from scipy.signal import find_peaks_cwt

def startIV(self):

    # Deshabilitar el botón Start
    self.start_button.configure(state="disabled")

    # Obtener los valores ingresados en los campos de entrada
    vStart = self.vStart.get()
    vStop = self.vStop.get()
    vStep = self.vStep.get()
    option = self.options.get()

    # Verificar si alguno de los campos está vacío
    if not vStart:
        vStart = 0
    if not vStop:
        vStop = -50
    if not vStep:
        vStep = 0.05
    
    print("Starting sweep from "+str(vStart)+"V to "+str(vStop)+"V at "+str(vStep)+"V step")

    if option == "SMU":
        #No tocar/Configuracion
        smu=lm.init_pyvisa("smu")

        del smu.timeout

        #Reset
        smu.write(ds.rst)
        #Configuration staircase sweep measure
        smu.write(ds.voltMode)
        smu.write(ds.sweepMode)
        smu.write(ds.sweepSing)
        smu.write(ds.sweepLin)
        smu.write(":SOUR:VOLT:STAR "+str(vStart))
        smu.write(":SOUR:VOLT:STOP "+str(vStop))
        points=int(abs(int(vStart)-int(vStop))/vStep)
        smu.write(":SOUR:VOLT:POIN "+str(points))

        #Set auto-range current measurement
        smu.write(ds.smuAuto1)
        smu.write(ds.smuAuto2)
        smu.write(ds.smuAuto3)

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
            
        result = [vValues, iValues]
        return result
    else:
        print("Not configured yet")


def startIVTEST(self):

    vStart = self.vStart.get()
    vStop = self.vStop.get()
    vStep = self.vStep.get()

    print("Starting sweep from "+str(vStart)+"V to "+str(vStop)+"V at "+str(vStep)+"V step")
    x = ["1.5", "1.2", "0.9","0.6", "0.3", "0","-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8", "-9", "-10"]
    y = ["8", "7", "6","5", "5", "5","-1", "-1", "-4", "-5", "-6", "-6", "-7", "-8", "-9", "-10"]
    #return [x,y]

    print(x)
    print(y)
    # Asignar un valor a la variable
    self.vValuesAux.set(" ".join(map(str, x)))
    self.iValuesAux.set(" ".join(map(str, y)))

    for num in range(len(y)):
        y[num]=float(y[num])
        x[num]=float(x[num])

    # Crear un nuevo lienzo (canvas) y configurar el grid
    fig = Figure(figsize=(6, 4), dpi=100)
    self.ax = fig.add_subplot(111)

    # Borrar el histograma anterior
    self.ax.clear()

    self.canvas = FigureCanvasTkAgg(fig, self.plotIV)
    self.canvas.get_tk_widget().grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    self.ax.plot(x, y)
    self.ax.set_xlabel('Voltage')
    self.ax.set_ylabel('Current')
    self.ax.set_title('IV Curve')
    fig.canvas.draw()

def saveResultsIV(self, path):

    vValues = self.vValuesAux.get()
    iValues = self.iValuesAux.get()
    
    try:
        vValues = vValues.split()
        iValues = iValues.split()
        lm.file_writer_iv(vValues, iValues, path)
        print("Guardado con exito en: "+path)
    except:
        print("Error al guardar.")

def save_plot_as_png(self):
    name = self.save_entry.get()
    path=lm.path(self.tabview.get())
    lm.create_dir(path)
    if not name:
        print("Introduzca un nombre antes de guardar.")
    else:
        filename = path + name + '.png'
        fig = self.canvas.figure
        fig.savefig(filename)
        print("Imagen guardada correctamente.")

def startSpectrum(self):

        if self.entries.get():
            
            try:
                # Deshabilitar el botón Start
                self.startSpec_button.configure(state="disabled")

                # Obtener el número de datos del entry self.entries
                num_datos = int(self.entries.get())

                # Crear un nuevo lienzo (canvas) y configurar el grid
                fig = Figure(figsize=(6, 4), dpi=100)
                self.ax = fig.add_subplot(111)

                # Borrar el histograma anterior
                self.ax.clear()

                self.canvas = FigureCanvasTkAgg(fig, self.liveplot)
                self.canvas.get_tk_widget().grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

                # Datos y contadores para el histograma
                x_values = []
                
                rta=lm.init_pyvisa("scope")
                rta.write("FORM BIN")
                channel=self.selected_channelSpec.get()
                print(ds.selectChanCur(channel))
                rta.write(ds.selectChanCur(channel))

                # Generar los datos aleatorios y actualizar el histograma
                for i in range(1, num_datos + 1):

                    if rta.query(ds.rdy):
                        p1=float(rta.query(ds.posC1))
                    if rta.query(ds.rdy):
                        p2=float(rta.query(ds.posC2))

                    r=(p1-p2)
                    x_values.append(r)

                    #Print de control
                    lm.counter_finish(len(x_values), num_datos)
                    if len(x_values) == 0:
                        break
                    self.update_idletasks()  # Actualizar la interfaz gráfica


                    if (i%100 == 0):
                        self.ax.clear()
                        self.ax.hist(x_values, bins=50)
                        #Print de control
                        lm.counter_finish(len(x_values), num_datos)
                        # Actualizar la imagen
                        self.canvas.draw()
                        self.update_idletasks()  # Actualizar la interfaz gráfica
                
                self.histData.set(x_values)
                

            except Exception as e:
                print("Error:", e)

            finally:
                # Habilitar el botón Start nuevamente al finalizar
                self.startSpec_button.configure(state="normal")
                self.valuesAux.set(" ".join(map(str, x_values)))
                lm.beep()
                print("Finish histogram.")
        else:
            print("Introduce un valor para entries primero.")

def startSpectrumTest(self):

        if self.entries.get():
            
            try:
                # Deshabilitar el botón Start
                self.startSpec_button.configure(state="disabled")

                # Obtener el número de datos del entry self.entries
                num_datos = int(self.entries.get())

                # Crear un nuevo lienzo (canvas) y configurar el grid
                fig = Figure(figsize=(6, 4), dpi=100)
                self.ax = fig.add_subplot(111)

                # Borrar el histograma anterior
                self.ax.clear()

                self.canvas = FigureCanvasTkAgg(fig, self.liveplot)
                self.canvas.get_tk_widget().grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

                # Datos y contadores para el histograma
                x_values = []

                # Generar los datos aleatorios y actualizar el histograma
                for i in range(1, num_datos + 1):
                    y = random.uniform(1, 3)
                    x_values.append(y)
                    y = random.uniform(1, 3)
                    x_values.append(y)
                    y = random.uniform(1, 3)
                    x_values.append(y)
                    y = random.uniform(3, 4)
                    x_values.append(y)
                    y = random.uniform(4, 6)
                    x_values.append(y)
                    y = random.uniform(4, 6)
                    x_values.append(y)
                    y = random.uniform(4, 6)
                    x_values.append(y)
                    y = random.uniform(6, 7)
                    x_values.append(y)
                    y = random.uniform(7, 9)
                    x_values.append(y)
                    y = random.uniform(7, 9)
                    x_values.append(y)

                    if (i%100 == 0):
                        self.ax.clear()
                        self.ax.hist(x_values, bins=100)
                        #Print de control
                        lm.counter_finish(len(x_values), num_datos)
                        # Actualizar la imagen
                        self.canvas.draw()
                        self.update_idletasks()  # Actualizar la interfaz gráfica
                
                self.histData.set(x_values)
                

            except Exception as e:
                print("Error:", e)

            finally:
                # Habilitar el botón Start nuevamente al finalizar
                self.startSpec_button.configure(state="normal")
                self.valuesAux.set(" ".join(map(str, x_values)))
                lm.beep()
                print("Finish histogram.")
        else:
            print("Introduce un valor para entries primero.")

def openResults(self):
    path = lm.path(self.tabview.get())
    try:
        path = path.replace("/", "\\")
        print("Ruta obtenida:", path[:-1])  # Imprimir la ruta obtenida
        
        # Obtener el nombre de la carpeta del camino
        folder_name = os.path.basename(path[:-1])

        # La carpeta no está abierta, abrir una nueva ventana
        os.system(f'explorer "{path[:-1]}"')
    except:
        print("No existe la ruta seleccionada.")

def saveResultsSpec(self, path, name):
    valuep = self.valuesAux.get()
    valuep = [float(val) for val in valuep.split()]  # Convertir los valores a números
    auxLen = np.arange(0 , len(valuep) , 1)
    try:
        with open(path + name +'.txt', 'w') as f:
            f.write(str(np.min(valuep)) + " " + str(np.max(valuep)) + "\n")
            for i in auxLen:
                f.write(str(valuep[i])+" ")
                #f.write('\n')
        print("Guardado con exito en: "+path)
    except:
        print("Error al guardar.")

def saveResults(self):

    name = self.save_entry.get()
    path=lm.path(self.tabview.get())
    if not name:
        print("Introduzca un nombre antes de guardar.")
    else:
        lm.create_dir(path)
        if self.tabview.get() == "IV Curves":
            path=path + name
            saveResultsIV(self, path)
        if self.tabview.get() == "Spectrum":
            saveResultsSpec(self, path, name)
        if self.tabview.get() == "Waveform":
            print("Esta funcion se guarda automaticamente")

def plotExampleSpec(self):
    fig = Figure(figsize=(6, 4), dpi=100)

    ax = fig.add_subplot(111)

    y = [1, 2, 3, 4, 5]

    ax.hist(y)

    self.canvas = FigureCanvasTkAgg(fig, self.liveplot)
    self.canvas.draw()
    self.canvas.get_tk_widget().grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

def plotExampleWf(self):
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)

    x = [1, 2, 3, 4, 5]
    y = [10, 10, 50, 40, 10]

    ax.plot(x, y)

    self.canvas = FigureCanvasTkAgg(fig, self.plotWf)
    self.canvas.draw()
    self.canvas.get_tk_widget().grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

def plotExampleIV(self):
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)

    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]

    ax.plot(x, y)

    self.canvas = FigureCanvasTkAgg(fig, self.plotIV)
    self.canvas.draw()
    self.canvas.get_tk_widget().grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

def startVbr(self, vbr_Output):

    vbr_Output.configure(state="normal")
    vbr_Output.delete("1.0", "end")
    # Asignar un valor a la variable
    vValues=self.vValuesAux.get()
    iValues=self.iValuesAux.get()

    if not vValues or not iValues: 
        print("Necesitas realizar algun analisis primero..")
    else:
        values_listx = vValues.split()
        values_listy = iValues.split()
        # Convertir cada elemento a float
        vValues = [float(x) for x in values_listx]
        iValues = [float(x) for x in values_listy]
        #Quedarse con los valores negativos
        x_negativas = [valor_x for valor_x, valor_y in zip(vValues, iValues) if valor_x < 0]
        y_negativas = [valor_y for valor_x, valor_y in zip(vValues, iValues) if valor_x < 0]

        #print(y_negativas)

        if not x_negativas or not y_negativas:
            print("No se encuentran valore adecuados para calcular Vbr.")
        else:
            vValues = x_negativas
            iValues = y_negativas
            # Dividir la cadena en elementos individuales utilizando espacios como separadores

            # Calcular las derivadas de v y i
            dy = np.diff(iValues) / np.diff(vValues)

            # Encontrar el índice de la máxima tangente
            max_index = np.argmax(dy)

            # Obtener el punto de máxima tangencia
            max_x = vValues[max_index]
            max_y = iValues[max_index]

            vbr_Output.insert("0.0", str(max_x)+" V")
            vbr_Output.configure(state="disabled")
            # Obtener la figura y el lienzo
            fig = self.canvas.figure

            # Dibujar el punto rojo en el lienzo
            self.canvas.draw()
            ax = fig.gca()
            ax.cla()
            ax.plot(x_negativas,y_negativas)
            ax.plot(max_x, max_y, 'ro')

            # Actualizar la figura
            fig.canvas.draw()

def startQr(self, qr_Output):
    qr_Output.configure(state="normal")
    qr_Output.delete("1.0", "end")
    # Asignar un valor a la variable
    vValues=self.vValuesAux.get()
    iValues=self.iValuesAux.get()

    if not vValues or not iValues: 
        print("Necesitas realizar algun analisis primero..")
    else:
        # Dividir la cadena en elementos individuales utilizando espacios como separadores
        values_listx = vValues.split()
        values_listy = iValues.split()
        # Convertir cada elemento a float
        vValues = [float(x) for x in values_listx]
        iValues = [float(x) for x in values_listy]
        #Quedarse con los valores positivos
        x_positivas = [valor_x for valor_x, valor_y in zip(vValues, iValues) if valor_x > 0]
        y_positivas = [valor_y for valor_x, valor_y in zip(vValues, iValues) if valor_x > 0]

        #print(y_positivas)

        if not x_positivas or not y_positivas:
            print("No se encuentran valore adecuados para calcular Qr.")
        else:
            vValues = [valor_x for valor_x, valor_y in zip(x_positivas, y_positivas) if valor_x > 0.75]
            iValues = [valor_y for valor_x, valor_y in zip(x_positivas, y_positivas) if valor_x > 0.75]
            print(iValues)
            print(vValues)

            # Calcular de QR ...
            m=(max(iValues)-min(iValues))/(max(vValues)-min(vValues))
            qr='%.1f' % round(1/m, 1)

            qr_Output.insert("0.0", str(qr)+" Ω")
            qr_Output.configure(state="disabled")
            # Obtener la figura y el lienzo
            fig = self.canvas.figure

            # Dibujar el ajuste recto en el lienzo
            self.canvas.draw()
            ax = fig.gca()
            ax.cla()
            ax.plot(x_positivas,y_positivas)
            x_values = [min(vValues), max(vValues)]
            y_values = [min(iValues), max(iValues)]
            ax.plot(x_values, y_values, 'ro', linestyle="--")

            # Actualizar la figura
            fig.canvas.draw()

def complete(self):
    # Asignar un valor a la variable
    vValues=self.vValuesAux.get()
    iValues=self.iValuesAux.get()
    if not vValues or not iValues: 
        print("Necesitas realizar algun analisis primero..")
    else:
        # Dividir la cadena en elementos individuales utilizando espacios como separadores
        values_listx = vValues.split()
        values_listy = iValues.split()
        # Convertir cada elemento a float
        vValues = [float(x) for x in values_listx]
        iValues = [float(x) for x in values_listy]
        # Obtener la figura y el lienzo
        fig = self.canvas.figure

        # Dibujar el ajuste recto en el lienzo
        self.canvas.draw()
        ax = fig.gca()
        ax.cla()
        ax.plot(vValues,iValues)

        # Actualizar la figura
        fig.canvas.draw()

def finding_peaks(self):

    # Definir una función gaussiana
    def gaussian(x, mu, sigma, height):
        return height * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
    
    values = self.histData.get()
    if not values:
        print("Primero debes de recoger datos que analizar.")
    else:
        # Eliminar paréntesis y espacios en blanco
        values = values.replace("(", "").replace(")", "").replace(" ", "")
        values_list = values.split(",")
        data = np.array([float(x) for x in values_list])

        # Limpiar el plot existente sin crear un nuevo lienzo
        self.ax.clear()

        # Histograma
        N, bins, patches = self.ax.hist(data, bins=50)

        fracs = N / N.max()

        norm = colors.Normalize(fracs.min(), fracs.max())

        for thisfrac, thispatch in zip(fracs, patches):
            color = plt.cm.viridis(norm(thisfrac))
            thispatch.set_facecolor(color)

        # Plot de líneas
        bins = bins[1:]
        self.ax.plot(bins, N)

        # Encontrar los picos
        peaks, _ = find_peaks(N, prominence=80)
        #print(peaks)

        # Plot de los picos como marcadores "x"
        self.ax.plot(bins[peaks], N[peaks], "rx")

        # Actualizar la imagen
        self.canvas.draw()
        self.update_idletasks()  # Actualizar la interfaz gráfica

def startWf(self):   

    entries=self.timeWf.get()

    if not entries or not self.save_entry.get():
        print("Introduce un valor a entries o nombre al fichero")
    else:
        name=self.save_entry.get()
        #Creacion de directorios por fechas y nombres
        path=lm.path("Waveform")
        lm.create_dir(path)
        pathD = path + name 
        lm.delete_dir(pathD)
        lm.create_dir(pathD)
        pathF = pathD + "/" + name
        lm.delete_dir(pathF)
        startTime=lm.currentTime()
        lm.chronometter(startTime, float(entries), self)
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

        for i in range(int(trigg)):
    
            rta.write(ds.selectCurr(trigg, i))
            y_aux=rta.query(ds.waveform(self.selected_channelWf.get()))
            #print(y_aux)
            y=[float(i) for i in y_aux.split(',')]

            lm.waiting(rta)

            tsr=rta.query(ds.tsr)

            lm.file_writer_wf(pathF, tsr, y, i) 
            lm.counter_finish(i, trigg)  
            self.update_idletasks()  # Actualizar la interfaz gráfica

        pathFD= pathD + "/DATA.txt"
        lm.delete_dir(pathFD)
        lm.create_data(pathFD, rta, startTime, len(y))
        lm.create_zip(pathD, name)
        self.pathWf.set(pathD)

        rta.close()
        lm.beep()
        # Crear los puntos para el gráfico con 3752 valores
        x = np.linspace(0, len(y), 4056)

        # Crear un nuevo lienzo (canvas) y configurar el grid
        fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = fig.add_subplot(111)

        # Borrar el histograma anterior
        self.ax.clear()

        self.canvas = FigureCanvasTkAgg(fig, self.plotWf)
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Plot de los nuevos datos
        self.ax.plot(x, y)

        # Configuración del gráfico
        self.ax.set_xlabel('Time(s)')
        self.ax.set_ylabel('Intensity(A)')

        # Actualizar la figura
        fig.canvas.draw()

def startWfTest(self):   

    entries=self.timeWf.get()

    if not entries or not self.save_entry.get():
        print("Introduce un valor a entries o nombre al fichero")
    else:

        lm.chronometter(lm.currentTime(), float(entries), self)

        path="C:\\Users\\Usuario\\Desktop\\Laboratorio\\Programacion-Automatizacion\\Pyvisa\\Output\\Waveform\\2023-05-17\\fbk_40v_ln2_caen\\fbk_40v_ln2_caen_0.txt"    
        with open(path, 'r') as file:
            lines = file.readlines()[2:]  # Saltar las dos primeras líneas

        data = [float(line.strip()) for line in lines]

        # Crear los puntos para el gráfico con 3752 valores
        x = np.linspace(0, len(data), 3752)
        y = np.interp(x, np.arange(len(data)), data)

        # Crear un nuevo lienzo (canvas) y configurar el grid
        fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = fig.add_subplot(111)

        # Borrar el histograma anterior
        self.ax.clear()

        self.canvas = FigureCanvasTkAgg(fig, self.plotWf)
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Plot de los nuevos datos
        self.ax.plot(x, y)

        # Configuración del gráfico
        self.ax.set_xlabel('Time(s)')
        self.ax.set_ylabel('Intensity(A)')

        # Actualizar la figura
        fig.canvas.draw()
def count_files(self):
    # Ruta de la carpeta
    path=self.pathWf.get()

    # Obtener la lista de archivos en la carpeta
    files = os.listdir("C:\\Users\\Usuario\\Desktop\\Laboratorio\\Programacion-Automatizacion\\Pyvisa\\Output\\Waveform\\2023-05-30\\0")

    # Contar los archivos con el prefijo deseado
    count = sum(1 for file in files if file.startswith(str(self.save_entry.get())+"_"))
    return count

def startDcr(self, dcr_Output):
    dcr_Output.configure(state="normal")
    dcr_Output.delete("1.0", "end")

    try:
        dcr=round(count_files()/(float(self.timeWf.get())*60),2)
        dcr_Output.insert("0.0", str(dcr)+" Hz")
    except:
        print("Imposible calcular el dcr..")

    
    dcr_Output.configure(state="disabled")

def slider_event(self, value):

    print(round(value))
    path=str(self.pathWf.get())+"/"+str(self.save_entry.get())+"_"+str(round(value))+".txt"

    with open(path, 'r') as file:
        lines = file.readlines()[2:]  # Saltar las dos primeras líneas

    data = [float(line.strip()) for line in lines]

    # Crear los puntos para el gráfico con 3752 valores
    x = np.linspace(0, len(data), 4056)
    y = np.interp(x, np.arange(len(data)), data)

    # Crear un nuevo lienzo (canvas) y configurar el grid
    fig = Figure(figsize=(6, 4), dpi=100)
    self.ax = fig.add_subplot(111)

    # Borrar el histograma anterior
    self.ax.clear()

    self.canvas = FigureCanvasTkAgg(fig, self.plotWf)
    self.canvas.get_tk_widget().grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Plot de los nuevos datos
    self.ax.plot(x, y)

    # Configuración del gráfico
    self.ax.set_xlabel('Time(s)')
    self.ax.set_ylabel('Intensity(A)')

    # Actualizar la figura
    fig.canvas.draw()

    # Cerrar todas las figuras excepto la actual
    #plt.close('all')
    #print(str(plt.get_fignums())+"figuras")
    #print("Número de figuras abiertas:", len(str(plt.get_fignums())))

def decrease_slider_value(self,count):
    current_value = round(self.sliderWf.get())
    if current_value > 0:
        new_value = current_value - 1
        self.sliderWf.set(new_value)
        print(self.sliderWf.get())
        path=str(self.pathWf.get())+"/"+str(self.save_entry.get())+"_"+str(round(self.sliderWf.get()))+".txt"

        with open(path, 'r') as file:
            lines = file.readlines()[2:]  # Saltar las dos primeras líneas

        data = [float(line.strip()) for line in lines]

        # Crear los puntos para el gráfico con 3752 valores
        x = np.linspace(0, len(data), 4056)
        y = np.interp(x, np.arange(len(data)), data)

        # Crear un nuevo lienzo (canvas) y configurar el grid
        fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = fig.add_subplot(111)

        # Borrar el histograma anterior
        self.ax.clear()

        self.canvas = FigureCanvasTkAgg(fig, self.plotWf)
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Plot de los nuevos datos
        self.ax.plot(x, y)

        # Configuración del gráfico
        self.ax.set_xlabel('Time(s)')
        self.ax.set_ylabel('Intensity(A)')

        # Actualizar la figura
        fig.canvas.draw()

def increase_slider_value(self,count):
    current_value = round(self.sliderWf.get())
    if current_value < count:
        new_value = current_value + 1
        self.sliderWf.set(new_value)
        print(self.sliderWf.get())
        path=str(self.pathWf.get())+"/"+str(self.save_entry.get())+"_"+str(round(self.sliderWf.get()))+".txt"

        with open(path, 'r') as file:
            lines = file.readlines()[2:]  # Saltar las dos primeras líneas

        data = [float(line.strip()) for line in lines]

        # Crear los puntos para el gráfico con 3752 valores
        x = np.linspace(0, len(data), 3752)
        y = np.interp(x, np.arange(len(data)), data)

        # Crear un nuevo lienzo (canvas) y configurar el grid
        fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = fig.add_subplot(111)

        # Borrar el histograma anterior
        self.ax.clear()

        self.canvas = FigureCanvasTkAgg(fig, self.plotWf)
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Plot de los nuevos datos
        self.ax.plot(x, y)

        # Configuración del gráfico
        self.ax.set_xlabel('Time(s)')
        self.ax.set_ylabel('Intensity(A)')

        # Actualizar la figura
        fig.canvas.draw()
        


        



