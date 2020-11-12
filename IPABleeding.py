import os
import argparse
import subprocess

# Variables

objection="<OBJECTION_DIR_PATH>"

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
""" + "\ndeveloped by icarot\nVersion: 0.0.1\n")

def setParam():
    # Define the parameters of the script.
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", help="Inform the app to make bleed")
    global args
    args = parser.parse_args()

def objectionExists():
    # Check if the command Objection is configured correctly.
    if not os.path.isfile(objection): 
        print("[ERROR] Please set the binary path of Objection in the variable 'objection' within IPABleeding.py")
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
    print("File created: " + filename + "\n###")

def runCommand(command):
    returnCommand = subprocess.run(command, shell=True, capture_output=True, text=True)
    return returnCommand

def getAppClasses():
    print("\nGetting all the classes...");
    command = objection + ' --gadget ' + args.app + ' run "ios hooking list classes"'
    returnCommand = runCommand(command)
    saveFile(returnCommand.stdout,"list_classes.txt")

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

#==========================================

# Main

scriptBanner()
setParam()
objectionExists()
paramAppPassed()
getAppClasses()
getNSUserDefaults()
getNSUrlCredentialStorage()
getInfoBinary()
getCookies()
getKeychainDump()
