# UGR_Lab
Code &amp; Scripts

Aquí se definirán los setups y dentro de cada código se explicará cada parte más en detenimiento.

IV Curve: 

Para las curvas IV se usará el multiplexor de RS232, la power supply TTI 355P o TTI PLH120P (dependiendo de Vbias) y el electrómetro.
Se deben conectar los RS232 de los dispositivos al multiplexor y este al ordenador por USB.
Para medir en directa solo hará falta conectar el positivo de la fuente de alimentación al ánodo del diodo, y el positivo del electrómetro al cátodo,
se cierra el circuito uniendo los negativos de ambos. Para inversa la corriente fluirá desde el positivo de la power supply al cátodo del LED. Para correr el script, recuerda que la medición de directa debe ser positiva y para inversa negativa, para ellos solo cambia el orden de los cables al medir desde el electrómetro. Para iniciar solo hay que darle al play, te pedirá nombre del fichero y empezara solo.
Recuerda activar el output de la powersupply y poner dentro del codigo el canal al que hayas conectado del multiplexor.

Charge Spectre: 

Para el espectrograma de cargas se necesita una fuente de luz (Generador de ondas + LED o pulsador LED de CAEN), una señal que medir y el osciloscopio.
Para esta adquisición se hace uso del LED, no solo para iluminar a nivel de SPE y acelerar la medición si no también para usarlo como trigger externo del osciloscopio, con ello podemos ver el pedestal además de las distintas curvas.
Dentro del osciloscopio hay que configurar la aplicación de matemáticas para que nos calcule la integral de la señal y también los V-Marker, estos son los cursores que delimitaran el área que queremos integrar, para ello seleccionaremos M1 (Matemáticas 1) como fuente para el V-Marker.
El programa funciona dándole al play, te pedirá nombre del fichero, número de entradas y si la impedancia del scope es de 50 Ohm. Para acelerar la medición una vez que hemos visto el histograma correcto solo hay que cerrar el plot y la adquisición acelerará sustancialmente.

Waveform DAQ:

Para la última adquisición solo se hará uso del scope y de la señal a medir. El script recoge ventanas de un tamaño especifico, se debe configurar el trigger para que sea 0.5V del SPE. Este debe realizarse en obscuridad absoluta. Al igual que los anteriores solo se debe dar al play para que funcione.

PT100 DAQ:

Para la adquisicion del PT100 el setup debe ser el mismo que para las curvas IV y darle al play.

Se ha comentado que los dispositivos de medición del banco se conectan por RS232, ni que decir que el scope debe de estar conectado por RJ45 al ordenador. La red + IP ya esta configurada si no se pretende cambiar.




