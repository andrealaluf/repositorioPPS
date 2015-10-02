import time
import threading
from Queue import Queue
from Data import Data
from Command import Command
from HumidityTemperatureClass import HumidityTemperature
import random

def readSensor(data):
    while 1:
        condition.acquire()
        frequency = sensor.getFrequency()
        if (sensor.getSenseFlag() == False) & (frequency == 0):
            condition.wait()
        else:
            condition.wait(frequency)
            print 'estoy sensando'
            data.put(sensor.getData('client'))
        condition.release()
        
def readData (data):
    while 1:
        print data.get(True).getData() 
        data.task_done()

def receiveCommand (command):
    while 1:
        comando = command.get(True)
        condition.acquire()
        if comando.getCommand() == 'SENSE':
            sensor.setSenseFlag(True)
        else:
            sensor.setSenseFlag(False)

        sensor.setFrequency(comando.getValue())
        if (sensor.getFrequency() > 0) | (sensor.getSenseFlag() == True):
            condition.notify()
        condition.release()
        command.task_done()
        time.sleep(0)
        
def setCommand (command):
    global frequency
    while 1:    
        commandValue = round(random.uniform(1,2))
        oldFrequency = frequency
        if commandValue == 1:
            frequency = random.uniform(5,10)
            command.put(Command('13','client','SETFR', frequency))
            print 'SETFR ', frequency
        else:
            command.put(Command('13','client','SENSE', oldFrequency))
            print 'SENSE'
        time.sleep(random.uniform(1,20))

try:
    if __name__=="__main__":
        pines = [4]    
        sensor = HumidityTemperature(0, pines)

        command = Queue(10)
        data = Queue(10)
        condition = threading.Condition()        
        frequency = 0

        dataThread = threading.Thread(target=readSensor, args = (data,)) 
        commandThread = threading.Thread(target=receiveCommand, args = (command,))
        escribircomando = threading.Thread(target=setCommand, args = (command,))
        leerDato = threading.Thread(target=readData, args = (data,))

        dataThread.start()
        commandThread.start()
        escribircomando.start()
        leerDato.start()

        while 1: pass
except KeyboardInterrupt:
    sensor.clearSensor()

