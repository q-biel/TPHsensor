from Tkinter import *
import time
import tkFileDialog
from Adafruit_BME280 import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure



sensor = BME280(mode=BME280_OSAMPLE_8)
root = Tk()
tempF = Figure(figsize=(4,3),dpi = 100)
a = tempF.add_subplot(111)
presF = Figure(figsize=(4,3),dpi = 100)
b = presF.add_subplot(111)
humF = Figure(figsize=(4,3),dpi = 100)
c = humF.add_subplot(111)

saving = 0
tempFile = 0



tempCanvas = FigureCanvasTkAgg(tempF,master=root)
tempCanvas.show()
presCanvas = FigureCanvasTkAgg(presF,master = root)
presCanvas.show()
humCanvas = FigureCanvasTkAgg(humF,master = root)
humCanvas.show()

x_data=[]
temp_data=[]
pres_data =[]
hum_data = []
time0 = 0
t = 0
p=0
h=0


temp = sensor.read_temperature()
press = sensor.read_pressure()/100
hum = sensor.read_humidity()
    
tempLabel = Label(root,text = "Temperature", font=('Helvetica',16)).grid(row=1,column=1, columnspan=7)
tempSens = Label(root,text = '{0:0.3f} deg C'.format(temp), font=('Helvetica',20))
tempSens.grid(row=2, column=1, columnspan=7)
tempCanvas.get_tk_widget().grid(row=3, column=1, columnspan=7)
presLabel = Label(root,text = "Pressure", font=('Helvetica',16)).grid(row=1,column=8, columnspan=7)
presSens = Label(root,text = '{0:0.2f} hPa'.format(press), font=('Helvetica',20))
presSens.grid(row=2,column=8, columnspan=7)
presCanvas.get_tk_widget().grid(row=3,column=8, columnspan=7)
humLabel = Label(root,text = "Humidity", font=('Helvetica',16)).grid(row=1,column=15, columnspan=7)
humSens = Label(root,text='{0:0.2f} %'.format(hum), font=('Helvetica',20))
humSens.grid(row=2,column=15, columnspan=7)
humCanvas.get_tk_widget().grid(row=3,column=15, columnspan=7)

varT=StringVar()
varP=StringVar()
varH=StringVar()



tempBut = Button(root, text="PATH", command=lambda:varT.set(tkFileDialog.askopenfilename()))
tempBut.grid(row=4, column=1)
presBut = Button(root, text = "PATH", command=lambda:varP.set(tkFileDialog.askopenfilename()))
presBut.grid(row=4, column=8)
humBut = Button(root, text="PATH", command=lambda:varH.set(tkFileDialog.askopenfilename()))
humBut.grid(row=4, column=15)

tempEn = Entry(root, textvariable=varT)
presEn = Entry(root, textvariable=varP)
humEn = Entry(root, textvariable=varH)
tempEn.grid(row=4, column=0, columnspan=8)
presEn.grid(row=4, column=9, columnspan=6)
humEn.grid(row=4, column=16, columnspan=6)


def dataOn():
    global saving
    global tempFile
    global presFile
    global humFile
    global time0
    global t, p, h
    saving=1
    time0 = time.mktime(time.gmtime())
    if tempEn.get():
        t=1
        tempFile = open(tempEn.get(),'w')
    if presEn.get():
        p=1
        presFile = open(presEn.get(),'w')
    if humEn.get():
        h=1
        humFile = open(humEn.get(),'w')


def dataOff():
    global saving
    global tempFile
    global presFile
    global humFile, t, p, h
    saving=0
    tempFile.close()
    presFile.close()
    humFile.close()
    t=0
    h=0
    p=0


aqStart = Button(root, text="Start", command=dataOn)
aqStop = Button(root, text = "Stop", command=dataOff)
aqStart.grid(row=5, column=1, rowspan=2, columnspan=3)
aqStop.grid(row=5, column=3, rowspan=2, columnspan=3)





def measure(tempSens,presSens,humSens, tempCanvas, presCanvas, humCanvas):
  
    def Meas():
        global x_data
        global temp_data
        global pres_data
        global hum_data
        global time0, t, p, h
        temp = sensor.read_temperature()
        press = sensor.read_pressure()/100
        hum = sensor.read_humidity()
        time1 = time.mktime(time.gmtime()) - time0

        if saving == 1:
            print str(time1)
            if t==1:
                tempFile.write(str(time1) + '\t' + str(temp) + '\n')
            if p==1:
                presFile.write(str(time1) + '\t' + str(press) + '\n')
            if h==1:
                humFile.write(str(time1) + '\t' + str(hum) + '\n')
            x_data +=[time1]
            temp_data+=[temp]
            pres_data+=[press]
            hum_data+=[hum]
            a.plot(x_data,temp_data,'b-')
            b.plot(x_data,pres_data,'b-')
            c.plot(x_data,hum_data,'b-')
            tempCanvas.show()
            presCanvas.show()
            humCanvas.show()
        
        tempSens.config(text = '{0:0.1f} deg C'.format(temp))
        presSens.config(text = '{0:0.0f} hPa'.format(press))
        humSens.config(text = '{0:0.2f} %'.format(hum))

        tempSens.after(60000,Meas)
    Meas()



measure(tempSens,presSens,humSens, tempCanvas, presCanvas, humCanvas)
root.mainloop()
