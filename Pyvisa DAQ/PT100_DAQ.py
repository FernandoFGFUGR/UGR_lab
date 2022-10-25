#Import librerias, algunas pueden estar sin usar.
import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import pyfirmata

def PT100(R):
    v = 31.64259588293078
    f = R

    v += f * 2.327765488883832
    f *= R

    v += f * 0.000825034783247256
    f *= R

    v += f * 5.503555111531539e-07
    f *= R

    v -= f * 8.846016370591097e-10
    f *= R

    v += f * 2.79478040084237e-12

    return v

def live_plotter(x_vec,y1_data,line1,identifier='',pause_time=0.1):
    if line1==[]:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(13,6))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(x_vec,y1_data,'-o',alpha=0.8)        
        #update plot label/title
        plt.ylabel('°C')
        plt.title('Temperature')
        plt.show()
    
    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(y1_data)
    # adjust limits if new data goes beyond bounds
    if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)
    
    # return line so we can update it again in the next iteration
    return line1

#Hacemos un listado de los puertos disponibles
rm = pyvisa.ResourceManager('@py')
rm.list_resources()

#Agregamos cada dispositivo al puerto donde esten conectados, Port1=ASRL5::INSTR, Port2=ASRL6::INSTR, Port3=ASRL7::INSTR, Port4=ASRL8::INSTR,
keithleyE = rm.open_resource('ASRL3::INSTR')
board = pyfirmata.Arduino('COM8')

#Ajustes de comunicacion
keithleyE.read_termination = '\n'
keithleyE.write_termination = '\n'
del keithleyE.timeout
keithleyE.baud_rate=9600

#Comandos SCPI para inicializar Keithley Electrometro
keithleyE.write("*RST")
keithleyE.write("SYST:ZCH ON")
keithleyE.write("FUNC 'RES'")
keithleyE.write("RES:RANG:AUTO ON")
keithleyE.write("SYST:ZCOR ON")
keithleyE.write("SYST:ZCH OFF")

# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')

size = 100
line1 = []
x_vec = np.linspace(0,1,size+1)[0:-1]
y_vec = np.zeros(len(x_vec))


while True:
    read=keithleyE.query_ascii_values('READ?', container=np.array)
    Rt=(round(read[0], 7))
    TempK = PT100(Rt)
    TempC = round((TempK - 273.15), 2)
    y_vec[-1] = TempC
    print(str(TempC) + ' °C')
    line1 = live_plotter(x_vec,y_vec,line1)
    y_vec = np.append(y_vec[1:],0.0)
    if (TempC > 30):
        board.digital[4].write(1)
    else:
        board.digital[4].write(0)