import os
import argparse
import subprocess

# Variables
objection="<OBJECTION_DIR_PATH>"
fridaps="<FRIDA-PS_DIR_PATH>"

#==========================================

def scriptBanner():
    print(""" 
                                                                                                        
@@@  @@@@@@@    @@@@@@      @@@@@@@   @@@       @@@@@@@@  @@@@@@@@  @@@@@@@   @@@  @@@  @@@   @@@@@@@@  
@@@  @@@@@@@@  @@@@@@@@     @@@@@@@@  @@@       @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@  @@@@ @@@  @@@@@@@@@  
@@!  @@!  @@@  @@!  @@@     @@!  @@@  @@!       @@!       @@!       @@!  @@@  @@!  @@!@!@@@  !@@        
!@!  !@!  @!@  !@!  @!@     !@   @!@  !@!       !@!       !@!       !@!  @!@  !@!  !@!!@!@!  !@!        
!!@  @!@@!@!   @!@!@!@!     @!@!@!@   @!!       @!!!:!    @!!!:!    @!@  !@!  !!@  @!@ !!@!  !@! @!@!@  
!!!  !!@!!!    !!!@!!!!     !!!@!!!!  !!!       !!!!!:    !!!!!:    !@!  !!!  !!!  !@!  !!!  !!! !!@!!  
!!:  !!:       !!:  !!!     !!:  !!!  !!:       !!:       !!:       !!:  !!!  !!:  !!:  !!!  :!!   !!:  
:!:  :!:       :!:  !:!     :!:  !:!   :!:      :!:       :!:       :!:  !:!  :!:  :!:  !:!  :!:   !::  
 ::   ::       ::   :::      :: ::::   :: ::::   :: ::::   :: ::::   :::: ::   ::   ::   ::   ::: ::::  
:     :         :   : :     :: : ::   : :: : :  : :: ::   : :: ::   :: :  :   :    ::    :    :: :: :   
""" + "\ndeveloped by icarot\nVersion: 0.0.2\n")

def setParam():
    # Define the parameters of the script.
    parser = argparse.ArgumentParser()
    mainOption = parser.add_mutually_exclusive_group()
    mainOption.add_argument("-a", "--app", metavar='<App>', help="Inform the app to make bleed.")
    mainOption.add_argument("-l", "--list", help="List the apps installed in the device using frida-ps.", action="store_true")
    parser.add_argument("-d", "--deep", help="This mode can take a long time to be completed. It will list all the methods from each class", action="store_true")
    parser.add_argument("-md", "--memdump", help="Will dump the memory of the app.", action="store_true")

    global args
    args = parser.parse_args()

def objectionExists():
    # Check if the command Objection is configured correctly.
    if not os.path.isfile(objection): 
        print("[ERROR] Please set the binary path of Objection in the variable 'objection' within IPABleeding.py")
        exit()

def fridapsExists():
    # Check if the command Frida-ps is configured correctly.
    if not os.path.isfile(fridaps):
        print("[ERROR] Please set the binary path of Frida-ps in the variable 'fridaps' within IPABleeding.py")
        exit()

def paramAppPassed():
    # Check if the app param was passed in the script execution.
    if args.app:
        print("Parameter informed...")
    else:
        print("Parameter was not informed...")
        exit()

def saveFile(data,filename):
    print("Creating a file...");
    file = open(filename, "w")
    file.write(data)
    file.close()
    if os.path.isfile(filename):
        print("File created: " + filename + "\n###")
    else:
        print("[ERROR] File " + filename + "was not created.\n###")

def runCommand(command):
    returnCommand = subprocess.run(command, shell=True, capture_output=True, text=True)
    if returnCommand.stderr:
        print("[ERROR] Error to run the command: " + command)
        print("[ERROR] Please verify if the Frida Server is up.")
        exit()
    else:
        return returnCommand

def lisApps():
    print("Getting all Apps installed in the iOS device...");
    fridapsExists()
    if args.list:
        command = fridaps + " -Uia"
        returnCommand = runCommand(command)
        print(returnCommand.stdout)
        exit()

def getAppClasses():
    print("Getting all the classes...");
    command = objection + ' --gadget ' + args.app + ' run "ios hooking list classes"'
    returnCommand = runCommand(command)
    saveFile(returnCommand.stdout,"list_classes.txt")

def getAppMethodClasses():
    print("Getting all methods for each class...");
    fileClasses = "list_classes.txt"
    fileMethod = "list_methods_per_class.txt"
    if os.path.isfile(fileClasses):
        fClass = open(fileClasses, "r")
        fMethod = open(fileMethod, "w")
        for lineClass in fClass:
            fMethod.write(lineClass)
            command = objection + ' --gadget ' + args.app + ' run "ios hooking list class_methods ' + lineClass +'"'
            returnCommand = runCommand(command)
            fMethod.write(returnCommand.stdout + "\n###\n")
    print("Creating a file...");
    if os.path.isfile(fileMethod):
        print("File created: " + fileMethod + "\n###")

def getNSUserDefaults():
    print("Getting NSUserDefaults...");
    command = objection + ' --gadget ' + args.app + ' run "ios nsuserdefaults get"'
    returnCommand = runCommand(command) 
    saveFile(returnCommand.stdout,"list_nsuserdefaults.txt")

def getNSUrlCredentialStorage():
    print("Getting NSUrlCredentialStorage...");
    command = objection + ' --gadget ' + args.app + ' run "ios nsurlcredentialstorage dump"'
    returnCommand = runCommand(command)
    saveFile(returnCommand.stdout,"list_nsurlcredentialstorage.txt")

def getInfoBinary():
    print("Getting binary info...");
    command = objection + ' --gadget ' + args.app + ' run "ios info binary"'
    returnCommand = runCommand(command)
    saveFile(returnCommand.stdout,"list_infobinary.txt")

def getCookies():
    print("Getting cookies...");
    command = objection + ' --gadget ' + args.app + ' run "ios cookies get"'
    returnCommand = runCommand(command)
    saveFile(returnCommand.stdout,"list_cookies.txt")

def getKeychainDump():
    print("Getting Keychains...");
    command = objection + ' --gadget ' + args.app + ' run "ios keychain dump"'
    returnCommand = runCommand(command)
    saveFile(returnCommand.stdout,"list_keychain.txt")

def dumpAppMemory():
    print("Dumping the App's data from memory...");
    if args.memdump:
        command = objection + ' --gadget ' + args.app + ' run "memory dump all dump.dmp"'
        returnCommand = runCommand(command)
        if os.path.isfile("dump.dmp"):
            print("File created: dump.dmp\n###")
        else:
            print("[ERROR] File 'dump.dmp' was not created.\n###")

def menuFlow():
    #Checks parameters passed in the script execution
    extraParam=False
    if args.list:
        lisApps()

    if args.app:
        if args.deep:
            extraParam=True
            getNSUserDefaults()
            getNSUrlCredentialStorage()
            getInfoBinary()
            getCookies()
            getKeychainDump()
            getAppClasses()
            getAppMethodClasses()
            dumpAppMemory()

        if args.memdump:
            extraParam=True
            dumpAppMemory()

        if extraParam == False:
            getNSUserDefaults()
            getNSUrlCredentialStorage()
            getInfoBinary()
            getCookies()
            getKeychainDump()
            getAppClasses()
    else:
        paramAppPassed()

#==========================================

# Main
scriptBanner()
setParam()
objectionExists()
menuFlow()
