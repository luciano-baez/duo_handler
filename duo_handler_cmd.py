# encoding: utf-8
## #!/usr/bin/python
#
# Copyright: (c) 2020, Luciano Baez <lucianobaez@ar.ibm.com>
#                                   <lucianobaez@outlook.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#  This is a module to handle /etc/sudoers file
#
# History
#   -Ver 0.1 : Aug 14 2020
#           - Implement the report option gets the sudo configuration as a dictionary.


import os
import sys
import datetime
# Importing all functions from repo lib sudo_handler_lib
from duo_handler_lib import getduo_fact 
from duo_handler_lib import addgrouptoduo
from duo_handler_lib import deletegroupfromduo
from duo_handler_lib import saveconfigfiles


# Variable Definition
#------------------------------------------------------------------------------------------------------------
# LogHandling
logdic = dict(
    log=False,
    logfile="/var/log/duo_handler"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".log"
    )

duo_fact={}
duo_handlercfg = dict(
    version="0.1",
    process=True,
    report=False,
    cmdusage=False,
    backup=True,
    savefiles=False
    )

scriptname="duo_handler_cmd"

#List of users to process
duo_module_addgroups=[]
duo_module_removegroups=[]
#List of unknown arguments
duo_module_argumentsnotdetected=[]

def cmduse():
    print ("Command usage: ")
    print ("  -? or -h              : Provides this output ")
    print ("  -report               : Provides a report without any change ")
    print ("  -savefiles            : Force to resave both files with the same information (/etc/duo/login_duo.conf and /etc/duo/pam_duo.conf) ")
    print ("                          using  /etc/duo/login_duo.conf as a source, generating a backup from the previuos files.")
    print ("  -addgroup=GROUP       : Adds a group in the config files in the 'groups=' clausule")
    print ("                          - If you want to add a group to be excluded from DUO you need to add the ! before the group ")
    print ("                          #"+scriptname+" -addgroup=!serviceusers ")
    print ("                          This will add at the end of the line of 'groups=' clausule, the !serviceusers exclude group ")
    print ("                          If you don't place the '!' negation simbol the user will not be excluded from duo. ")
    print ("  -removegroup=GROUP    : Removes a group from the config files in the 'groups=' clausule")
    print ("                          - If you want to remove a group from the DUO configuration files you could just use the group name")
    print ("                          #"+scriptname+" -removegroup=serviceusers ")
    print ("                          This will remove from the 'groups=' clausule, the 'serviceusers'  group even if its apears as '!serviceusers' ")


# Processs Arguments
#------------------------------------------------------------------------------------------------------------
# Count the arguments
arguments = len(sys.argv) - 1
# Output argument-wise
position = 1
insuficientarguments=False
if arguments == 0:
    # Print cmd usage
    cmdusage=1

if arguments==0:
    duo_handlercfg['cmdusage']=True
print (scriptname+" Ver:"+duo_handlercfg['version']+" ")
paramargs=[]
paramargs.append("")
paramargs.append("")
paramargs.append("")
paramargs.append("")
while (arguments >= position):
    argunknown=True
    arg=sys.argv[position]
    #print ("Parameter %i: %s" % (position, arg))
    argcomponents=arg.strip().split('=')
    directive=argcomponents[0]
    if len(argcomponents)>1:
        directiveargs=argcomponents[1].strip().split(',')
    else:
        aux=",,"
        directiveargs=aux.strip().split(',')
    # Hadling Help
    if directive == "-h":
        duo_handlercfg['cmdusage']=True
        argunknown=False
    if directive == "-?":
        duo_handlercfg['cmdusage']=True
        argunknown=False
    # Hadling actions
    if directive == "-report":
        duo_handlercfg['report']=True
        argunknown=False
    if directive == "-r":
        duo_handlercfg['report']=True
        argunknown=False
    if directive == "-savefiles":
        duo_handlercfg['savefiles']=True
        argunknown=False

    if directive == "-addgroup":
        duo_module_addgroups.append(argcomponents[1])
        argunknown=False
    if directive == "-removegroup":
        duo_module_removegroups.append(argcomponents[1])
        argunknown=False

    #Process unknown arguments
    if argunknown == True:
        duo_module_argumentsnotdetected.append(directive)
    position = position + 1



# Processing Detected Arguments
#------------------------------------------------------------------------------------------------------------
if duo_handlercfg['process']==True:
    #Getting duo Facts
    duo_fact=getduo_fact (logdic)

    # Detect if have sudo
    if duo_fact['installed']== True:

        if (len(duo_module_argumentsnotdetected)==0) :
            #Processing arguments without errors
            
            # Adding users to the cfg files
            for group in duo_module_addgroups:
                duo_handlercfg['savefiles']= True
                print("INF: Adding group "+group+" to DUO.")
                RC=addgrouptoduo(group,duo_fact,logdic)
                print(RC['stdout'])
            
            # Removing users from the cfg files
            for group in duo_module_removegroups:
                duo_handlercfg['savefiles']= True
                print("INF: Removing group "+group+" from DUO.")
                RC=deletegroupfromduo(group,duo_fact,logdic)
                print(RC['stdout'])

            # Printing report
            if duo_handlercfg['report']== True:
                print(duo_fact)

            # Saving files
            if duo_handlercfg['savefiles']== True:
                print("INF: Saving CFG to files /etc/duo/login_duo.conf and /etc/duo/pam_duo.conf")
                RC=saveconfigfiles(duo_fact,logdic)
                print(RC['stdout'])
        else:
            # Error Handling
            if (len(duo_module_argumentsnotdetected)>0):
                print("ERR: Argument Error.")

            duo_handlercfg['cmdusage'] = True
            print('')
            #Processing unknwon arguments
            for uargu in duo_module_argumentsnotdetected:
                print("ERR: Argument "+uargu+" not recognized.")
            print('')

    else:
        print("ERR: DUO not installed")    
#Handling Help
if duo_handlercfg['cmdusage'] == True:
    cmduse()
#------------------------------------------------------------------------------------------------------------
