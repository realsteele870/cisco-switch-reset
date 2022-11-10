import imp
import io
import os
from sqlite3 import connect
from time import sleep

import serial


def openSerialConnection(baudrate, port):
    ser = serial.Serial()
    ser.baudrate = baudrate
    ser.port = port
    ser.open()
    return ser
def sendToConsole(ser: serial.Serial, command: str, wait_time: float =3):
    command_to_send = " "+command+"\r"
    data_str=""
    ser.write(command_to_send.encode('Utf-8'))
    sleep(wait_time)
    while (ser.inWaiting()>0):
        data_str =data_str+ ser.read(ser.inWaiting()).decode('ascii')
       
    print(data_str, end="")
    return data_str
class connectionClass():
    
    
    def __init__(self):
        self.rate = input("Enter baudrate: ")
        self.port = input("Enter port: ")
        

def Welcome():
    print("Welcome to cisco switch reset version 1 By Remington Steele\n")
    return connectionClass()

def CheckConnection(ser: serial.Serial, check: str):
    connectionCheck = sendToConsole(ser,"")
    if (connectionCheck == check):
        return False
    return True

def containsCheckConnection(ser: serial.Serial, check: str):
    connectionCheck = sendToConsole(ser,"")
    if (connectionCheck.__contains__(check)) :
        return False
    return True
def breakConnection(ser):
    result=sendToConsole(ser,"")



    while (not (result.__contains__("Initializing Flash..."))) or (result.__contains__("switch:")):
        print(result)
        result = sendToConsole(ser,"")
    
    ser.send_break(1)
    sendToConsole(ser, "")
def splitDirectory(ciscoDir):
    Ciscoarr = ciscoDir.split()
    x=1
    newArray = []

    for  value in Ciscoarr:
        
        
        
        if (value == "<date>"):
           if(not Ciscoarr[x].endswith(".bin")):
             newArray.append(Ciscoarr[x])

        x=x+1
       
    
    for value in newArray:
        print(value)

    return newArray

def main():
    ConnectClass = Welcome()
   # print(ConnectClass.rate+ConnectClass.port)
    Connection = openSerialConnection(ConnectClass.rate,ConnectClass.port)
    bootDone = CheckConnection(Connection,"")
    print("Booting up...")
    while bootDone == False:
        print(".")
        bootDone = CheckConnection(Connection,"")
    input("ready? break it out :D")
    sendToConsole(Connection,"flash_init")
    sleep(30)
    sendToConsole(Connection,"")

    while (Connection.inWaiting()>0):
        data_str = Connection.read(Connection.inWaiting()).decode('ascii')
        print(data_str, end="")
    Connection.flush()



    
   # print(Connection.readline())
   
    
    sleep(5)
    ciscoDir =sendToConsole(Connection,"dir flash:")
    filesToRemove =splitDirectory(ciscoDir)





    
    
    Connection.close()


   

if __name__=="__main__":
    main()
    


