import imp
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
def sendToConsole(ser: serial.Serial, command: str, wait_time: float =1):
    command_to_send = " "+command+"\r"
    ser.write(command_to_send.encode('Utf-8'))
    sleep(wait_time)
    recievedText =ser.read(ser.inWaiting()).decode('utf-8')
    print(recievedText)
    return recievedText
class connectionClass():
    
    
    def __init__(self):
        self.rate = input("Enter baudrate: ")
        self.port = input("Enter port: ")
        

def Welcome():
    print("Welcome to cisco switch reset version 1 By Remington Steele\n")
    return connectionClass()

def CheckConnection(ser: serial.Serial):
    connectionCheck = sendToConsole(ser,"")
    if connectionCheck == "":
        return False
    return True
def breakConnection(ser):
    result=CheckConnection(ser)
    
    while result ==False:
        print(result)
        result = CheckConnection(ser)
    
    
    ser.send_break(2)
    sendToConsole(ser, "")

    
def main():
    ConnectClass = Welcome()
   # print(ConnectClass.rate+ConnectClass.port)
    Connection = openSerialConnection(ConnectClass.rate,ConnectClass.port)
    breakConnection(Connection)


    
    
    Connection.close()


   

if __name__=="__main__":
    main()
    


