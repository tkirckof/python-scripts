#!/usr/bin/python
##Author Name - Thomas Kirckof
##Author Email - tom.kirckof@purestorage.com
##Purestorage Rest API script used to manage the over-write of a single protection group using a replicated snapshot.
##This tool can quickly be modified to support the management of multiple replicated protection groups
import purestorage
import os
import time
import sys
import signal
import pprint
global option
pp=pprint.PrettyPrinter()

##IP addresses of the source and production arrays.
##These need to be changed to the actual Pure Storage array VIP addresses being used by the customer.
drip = ("10.234.112.100")
prodip = ("10.234.112.107")

##Authentication via API token keys.
##These need to be updated with the pureuser API key from the customers Prod and DR array.
drarray = purestorage.FlashArray(drip, api_token = "bcbdab78-d118-1c8d-9310-63d801f4069d")
prodarray = purestorage.FlashArray(prodip, api_token = "5f6bf716-f0a7-8e1b-aefd-865a55ae094b")

##Main display menu listing options available in the tool.
##No changes should be required here unless you decide to add a new function.
def mainmenu():
	global option
	os.system('clear')
	print ("\n DR Management Utility                   Array's "+prodip+" & "+drip+" Have Been Selected\n\n")
        print (" 1.)List Replicated Protection Group     2.)List Replicated Protection Group Snapshots\n\n")
        print (" 3.)Snapshot Prod PG & Replicate Now     4.)Over-write DR Protection Group\n\n")
        print (" 5.)Disconnect Volumes From DR Host      6.)Connect Volumes To DR Host\n\n")
        print (" 99.)Exit DR Management Utility\n\n")
	option=int(raw_input("\n Enter Task # "))
        choice()

##Choice function to define which function is called based on the selection for the mainmenu() function.
##No changes required here unless you add new functions to the tool.
def choice():
	global option
	if option == 1:
		list_pgroups()
	elif option == 2:
		list_pg_snaps()
	elif option == 3:
		snap_pgroup()
	elif option == 4:
		pgroup_overwrite()
	elif option == 5:
		disconnect_volumes()
	elif option == 6:
		connect_volumes()
	elif option == 99:
		quit()
        elif (option >= 7):
                os.system('clear')
                print ("\nYou Made An Invalid Selection Please Try Again.\n")
                time.sleep(1)
                mainmenu()
		
##list_groups() function that displays the status of the target protection group from the DR array.
##You will have to change the name of the protection group in the sourcegrp line of code.
def list_pgroups():
        os.system('clear')
        sourcegrp = "nypure002:EDG-SVDATA6VG-PROD"
        pgrouplist = drarray.list_pgroups(names=sourcegrp)
        os.system('clear')
        pp.pprint(pgrouplist)
        raw_input("\nPress the enter key to continue.")
        mainmenu()

##list_pg_snaps() function that list the replicated snapshots on the DR array for the defined protection group.
##You will have to change the name of the protection group assigned to the sourcegrp variable.
def list_pg_snaps():
	os.system('clear')
        sourcegrp = "nypure002:EDG-SVDATA6VG-PROD"
        pgroup_snap_list = drarray.list_pgroups(names=sourcegrp, snap = "true")
        os.system('clear')
        pp.pprint(pgroup_snap_list)
        raw_input("\nPress the enter key to continue.")
        mainmenu()

##snap_pgroup() funtion will take a snapshot of the production protection group on the production array and replicate it now to the DR array.
##You will have to change the name of the protection group assigned to the sourcegrp variable.
def snap_pgroup():
	os.system('clear')
        sourcegrp = "EDG-SVDATA6VG-PROD"
        print ("\nA New Snapshot Will Created For The Production Protection Group "+sourcegrp)
        raw_input("\nPress the enter key to continue or cntl-c to abort.")
        prodarray.create_pgroup_snapshot(sourcegrp, replicate_now="true")
        raw_input("\nPress the enter key to continue.")
        mainmenu()
       
##pgroup_overwrite function overwrites the DR protection group with the selected snapshot image. You first have to disconnect all of the volumes from the host.
##You will have to change the protection group name assigned to the targetgrp variable.
def pgroup_overwrite():
	os.system('clear')
        targetgrp = "svdata6vg-DR"
        sourcesnap = raw_input("Enter Aggregate Snapshot Name To Overwrite DR Protection Group With: ")
        print ("\nWarning !!! - The Following Protection Group Is About To Be Overwritten: "+targetgrp)
        print ("\nThe Protection Group Will Be Overwritten Using Aggregate Snapshot:  "+sourcesnap)
        raw_input("\nPress the enter key to continue or cntl-c to abort.")
        drarray.create_pgroup(targetgrp, overwrite="true", source=sourcesnap)
        raw_input("\nPress the enter key to continue.")
        mainmenu()

##disconnect_volumes function disconnects the volumes from the selected hosts.
##The hosts,volnum, and volname variables will have to be modified. Note that the volnum variable was designed to support a 2 digit volume name extension.
def disconnect_volumes():
        os.system('clear')
        host = "svdata6vg-DR"
        volnum = ["%02d" % x for x in range(01, 26)]
        print ("\nWarning !!! - All Database Volumes From Host "+host+" Are About To Be Disconnected")
        print ("\nWarning !!! - Make Sure All Volumes Are Unmounted From Host "+host+" Before Proceeding")
        raw_input("\nPress the enter key to continue or cntl-c to abort.")
        for i in volnum:
            volname="svdata6vg-"+(i)
            drarray.disconnect_host(host, volname)
            print ("Volume "+volname+" Has Been Disconnected From Host: "+host)
        raw_input("\nPress the enter key to continue.")
        mainmenu()

##connect_volumes function connects the volumes to the selected hosts.
##The hosts,volnum, and volname variables will have to be modified. Note that the volnum variable was designed to support a 2 digit volume name extension.
def connect_volumes():
        os.system('clear')
        host = "svdata6vg-DR"
        volnum = ["%02d" % x for x in range(01, 26)]
        for i in volnum:
            volname="svdata6vg-"+(i)
            drarray.connect_host(host, volname)
            print ("Volume "+volname+" Has Been Connected To Host: "+host)
        raw_input("\nPress the enter key to continue.")
        mainmenu()

mainmenu()
