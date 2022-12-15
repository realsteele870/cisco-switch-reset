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
    if (command=="y") or (command==""):
        command_to_send = command+"\r"

    
    data_str=""
    ser.write(command_to_send.encode('Utf-8'))
    sleep(wait_time)
    while (ser.inWaiting()>0):
        data_str =data_str+ ser.readline(ser.inWaiting()).decode('ascii')
        
       
    print(data_str, end="",flush=True)
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
    if (check in connectionCheck) :
        return True
    return False
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
       
    print("array start: \n\n")
    for value in newArray:
        print(value)

    return newArray

def deleteFiles(filesToDelete,ser):
    
    command = "del "
    for file in filesToDelete:
        command= command + "flash:"+file+" "
    sendToConsole(ser,command)

    for file in filesToDelete:
        sendToConsole(ser,"y")

def fileOutput(Text, check):
    verArr= Text.split()
    
    x=0
    returnText=""

    for word in verArr:
        if(word == check):
            returnText= word+": "+verArr[x+1]
        x=x+1

    

    return returnText

def memFileOutput(Text, check):
    verArr= Text.split("\n")
    
    x=0
    returnText=""

    for line in verArr:
        if(check in line):
            returnText= line
            
        x=x+1

    

    return returnText
def runSwitch(Connection: serial.Serial):
    bootDone = (containsCheckConnection(Connection,"Initializing Flash") or containsCheckConnection(Connection,"switch:")) 
    print("Booting up...",end="",flush=True)
    while bootDone == False:
        print(".",end ='',flush=True)
        bootDone = (containsCheckConnection(Connection,"Initializing Flash") or containsCheckConnection(Connection,"switch:")) 
    
    input("ready? break it out :D")

    Connection.reset_output_buffer()
    Connection.flushOutput()
    bootDone = containsCheckConnection(Connection,"switch:")
    while bootDone ==False:
        bootDone=containsCheckConnection(Connection,"switch:")
    sendToConsole(Connection,"flash_init")
    bootDone = containsCheckConnection(Connection,"switch:")
    while bootDone ==False:
        bootDone=containsCheckConnection(Connection,"switch:")
    #sleep(30)
    sendToConsole(Connection,"")

    while (Connection.inWaiting()>0):
        data_str = Connection.read(Connection.inWaiting()).decode('ascii')
        print(data_str, end="")
    Connection.flush()
    sleep(5)
    ciscoDir =sendToConsole(Connection,"dir flash:")
    filesToRemove =splitDirectory(ciscoDir)
    deleteFiles(filesToRemove,Connection)
    Connection.reset_output_buffer()
    sendToConsole(Connection,"boot")
    Connection.reset_output_buffer()
    bootDone = containsCheckConnection(Connection,"Would you like to enter the initial configuration dialog? [yes/no]:")
    while bootDone ==False:
        bootDone = containsCheckConnection(Connection,"Would you like to enter the initial configuration dialog? [yes/no]:")

    sendToConsole(Connection,"no")
    while (Connection.inWaiting()>0):
        data_str = Connection.read(Connection.inWaiting()).decode('ascii')
        print(data_str, end="")
    Connection.reset_output_buffer()
    versionText =sendToConsole(Connection,"show version | include Cisco")
    versionText=fileOutput(versionText,"Version")
    while (Connection.inWaiting()>0):
        data_str = Connection.read(Connection.inWaiting()).decode('ascii')
        print(data_str, end="")
    Connection.reset_output_buffer()
    memoryText =sendToConsole(Connection,"show version | include memory")
    memoryText = memFileOutput(memoryText,"bytes of flash-simulated non-volatile configuration memory")

    sendToConsole(Connection,"en")
    sendToConsole(Connection,"write erase")
    sendToConsole(Connection,"")
    #fileOutput(Connection,versionText,memoryText)
    f = open("switchOutput.txt","w")
    f.write("version: \n"+versionText)
    f.close()

    f= open("switchOutput.txt","a")
    f.write("\nmemory: \n"+memoryText)
    f.close()
    
def runRouter(Connection: serial.Serial):
    doneBreak=containsCheckConnection(Connection,"rommon 1 >")
    while doneBreak==False:
        Connection.send_break()
        doneBreak=containsCheckConnection(Connection,"rommon 1 >")

    sendToConsole(Connection,"confreg 0x2142") 
    sendToConsole(Connection,"reset")

    doneBoot = containsCheckConnection(Connection,"Router>")
    while doneBoot == False:
        doneBoot = containsCheckConnection(Connection,"Router>")

    sendToConsole(Connection,"en")
    sendToConsole(Connection,"write erase")
    sendToConsole(Connection,"")

    Connection.reset_output_buffer()
    versionText =sendToConsole(Connection,"show version | include Cisco")
    versionText=fileOutput(versionText,"Version")
    while (Connection.inWaiting()>0):
        data_str = Connection.read(Connection.inWaiting()).decode('ascii')
        print(data_str, end="")
    Connection.reset_output_buffer()
    memoryText =sendToConsole(Connection,"show version | include memory")
    memoryText = memFileOutput(memoryText,"bytes of non-volatile configuration memory")

    f = open("routerOutput.txt","w")
    f.write("version: \n"+versionText)
    f.close()

    f= open("routerOutput.txt","a")
    f.write("\nmemory: \n"+memoryText)
    f.close()

    sendToConsole(Connection, "config t")
    sendToConsole(Connection,"config-register 0x2102")
    sendToConsole(Connection,"end")
    sendToConsole(Connection,"reload")



    
    return

def main():

    ConnectClass = Welcome()
   # print(ConnectClass.rate+ConnectClass.port)
    Connection = openSerialConnection(ConnectClass.rate,ConnectClass.port)
    isDone = True
    selection=0
    while True:

        selection =input("Would you like to reset a\n 1)Switch\n 2)Router \n (1/2)\n")
        if (selection == "1") or (selection == "2"):
            break
        else:
            print("\nPlease type 1 or 2")

    while (isDone):
        if selection == "1":
            runSwitch(Connection,isDone)
        else:
            runRouter(Connection)


        
        
        
        
        DoneCheck = input("\nDone? y/n \n")
        if(DoneCheck=="y" or DoneCheck=="Y" or DoneCheck=="Yes" or DoneCheck=="yes" or DoneCheck=="YES"):
            isDone=False
            Connection.close()


   

if __name__=="__main__":
    main()
    


