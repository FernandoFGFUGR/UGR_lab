numCounts="ACQ:AVA?"
ascii="FORM ASCii"
lsbf="FORM:BORD LSBF"
#waveform="CHAN:DATA?"
rdy="*OPC?"
idn="*IDN?"
tsr="CHAN:HIST:TSR?"
lvlTrigger="TRIGger:A:LEVel1?"
arate="ACQuire:POINts:ARATe?"
srate="ACQuire:SRATe?"
timeBase="TIMebase:SCALe?"
saveTS="EXPort:ATABle:SAVE"
pulse="C1:BSWV WVTP,PULSE"
Bin="FORM BIN"
posC1="CURSor1:Y1Position?"
posC2="CURSor1:Y2Position?"
rst="*RST"
voltMode=":SOUR:VOLT:MODE VOLT"
sweepMode=":SOUR:VOLT:MODE SWE"
sweepSing=":SOUR:SWE:STA SING"
sweepLin=":SOUR:SWE:SPAC LIN"
smuAuto1=":sens:func ""curr"""
smuAuto2=":sens:curr:nplc 0.1"
smuAuto3=":sens:curr:prot 0.01"
smuTrig=":trig:sour aint"
smuOn=":outp on"
smuInit=":init (@1)"
queryCurr=":fetc:arr:curr? (@1)"
queryVolt=":fetc:arr:volt? (@1)"
smuOff=":outp off"

def selectCurr(trigg, i):
    return "CHAN:HIST:CURR " + str(-int(trigg)+(i+1))

def selectCurrMath(trigg, i):
    return "CALC:MATH1:HIST:CURR " + str(-int(trigg)+(i+1))

def waveform(channel):
    return "CHAN"+channel+":DATA?"

def waveformMath(channel):
    return "CALC:MATH"+channel+":DATA?"
