# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 12:06:47 2016

@author: phil
"""
#
#################################################################################
#This script executes a series of visual quality control procedures for MRI data.
#Built for the IMAGEN data set
#The user is required to have the following software libraries:
#	* python2.x, numpy
#	* AFNI-->installed in the default "abin" directory
##################################################################################
import sys,os
from fnmatch import fnmatch
from numpy import genfromtxt
from numpy import argwhere
import time,datetime
#
print "\n+++++++++++++++++++++++++++++++++++++++++++++"
print "+++++  Running Phil Spechler's Visual QC  +++++"
print "+++++     ~~ Updated! Version 2.8 ~~      +++++"
print "+++++++++++++++++++++++++++++++++++++++++++++++\n" 
#
#
##########################
#####   Set Paths   ######
##### Get Log Files ######
##### Get User info ######
##########################
#
##########################################################################################
# Set workdir to wherever the directory is located and cd to it	#
# Workdir should contain the following files--
#	(1.) this python script you're reading now
#	(2.) hotsub.txt --> a one-line textfile of the subject ID being inspected (start with 0) 
#	(3.) allsubs.txt --> a newline delimited textfile containing all subject IDs to QC
#	(4.) logfile.csv --> the logfile where QC metrics are saved
##########################################################################################
#Trailing backslash is needed at the end of the directory name
workdir='/Users/phil/Desktop/vis_QC_tools/'
os.chdir(workdir)
###############################################################################
#Set path to MRI datasets
#Expects the following directory structure:
# |------> path2anat -or- path2fmri
#      |------> subjectID directory
#          |------> whole-brain anatomical or functional images
##############################################################################
path2anat='/Volumes/Documents/Data/Imagen/Neuroimaging/Baseline_VBM_version2/'
###############################################################################
#Set path to fMRI datasets
path2fmri='/Volumes/Documents/Data/Imagen/Neuroimaging/fMRI_BSL_UpdatedModel/'
###############################################################################
#Set path to a backup directory. This is where the csv report will be backed up
#Trailing backslash is needed at the end of the directory name
path2backup='/Users/phil/Desktop/BACKUP_vis_QC_tools/'
###############################################################################
#Give name of CSV File to Write to. 
# *** This file is saved in the path2backup directory! ^
logfile='logfile.csv'
###############################################################################
#Import text file containing all subject ID numbers. 
#This should be a newline delimited list of all subjects ID #s
allsubs=genfromtxt('allsubs.txt',dtype='str')
###############################################################################
#Set list of acceptable inputs from the user
#Possible "yes", "no", and "check" answers allowed as inputs into terminal
##
yes=['yes','0','y','yeah','yea','yas','yep']
no=['no','1','nope','n0','nah','na','neg','n']
check=['9','check','chec','chek']
#
#
##########################################################################	
##################### Initialize QC FUNCTIONS ############################
#
#
##################################################################
# **Check anat displays the whole-brain anatomical 'mu*' image   # 
##################################################################
def check_anat():
	#prompt
	print "1.)Set mu* as the underlay (Should be automatic)"
	print "2.)Check for Anatomical Abnormalities"
	print "3.)Check for signal distortion and motion"
	print "\n**Scroll thru each view to check for quality and problems**"
	#Call up afni with dset loaded for visualization
	for file in os.listdir('.'):
		if fnmatch(file,'mu*'):
			os.system('afni -dset '+file+' &>/dev/null')#Using +' &>/dev/null' to suppress afni stdout  
	#promt
	print "\nIs the Anatomy ok?"
	#Get diagnosis
	#Get good (0) bad (1) or check (9) entry
	anatGB=raw_input("Enter 0=Yes ; 1=NO ; or 9=Check: ").lower()
	#################
	## Check Input ##
	#################	
	while anatGB not in yes+no+check:
		print "\nI don't follow your logic... Invalid input."
		print "\t\tTry again, {0}".format(user)
		print "\nIs the Anatomy ok?"			
		anatGB=raw_input("Enter 0=Yes ; 1=NO ; or 9=Check: ").lower()
	############################
	if anatGB in yes:
		anatGB='0'
	elif anatGB in no:
		anatGB='1'
	elif anatGB in check:
		anatGB='9'
	############################
	#Get comment string
	anatNote=raw_input("\n\tAny comments on anatomical to add?: ")
	#Remove commas so it doesn't screw up the csv format
	anatNote=anatNote.replace(',',' ')
	#append commas for csv
	anatGB=anatGB+','
	anatNote=anatNote+' ,'
	#Change to False for checking
	if '9' in anatGB:
		anatGB='False,'
	#Send out for logging
	loganat=anatGB+anatNote
	return loganat
############################################################################
# **Check GM displays the smoothed whole-brain gray matter image 'smwc1*'  #
############################################################################
def check_GM():
	print "###############################"
	print "Check Gray Matter Segmentation"
	print "###############################"
	print "\n1.)Load smwc1* as the underlay (Should be automatic)"
	print "\n2.)Check for completeness and quality of data"
	print "\n3.)Load MNI152_T1* as underlay"
	print "\n4.)Load smwc1* as overlay"
	print "\n5.)Check coregistration. Toggle overlay on/off"
	for file in os.listdir('.'):
		if fnmatch(file,'smwc1*'):
			os.system('afni -dset '+file+' ~/abin/MNI152_T1_2009c+tlrc.'+' &>/dev/null')
	print "\n"*2
	print "Is the GM Segmentation ok?" 
	GM_GB=raw_input("Enter 0=Yes ; 1=NO ; or 9=Check: ").lower()
	############################
	## Check Input for errors ##
	############################
	while GM_GB not in yes+no+check:
		print "\nI don't follow your logic... Invalid input."
		print "\t\tTry again, {0}".format(user)
		print "\nIs the GM Segmentation ok?"
		GM_GB=raw_input("Enter 0=Yes ; 1=NO ; or 9=Check: ").lower()
	##########################
	if GM_GB in yes:
		GM_GB='0'
	elif GM_GB in no:
		GM_GB='1'
	elif GM_GB in check:
		GM_GB='9'	
	###########################
	GM_GBNote=raw_input("\tAny comments on GM segmentation to add?: ")
	GM_GBNote=GM_GBNote.replace(',',' ')
	print "\n"
	print "Is the GM Coregistration ok?"
	GM_CoReg=raw_input("Enter 0=Yes ; 1=NO ; or 9=Check: ").lower()
	############################
	## Check Input for errors ##
	############################
	while GM_CoReg not in yes+no+check:
		print "\nI don't follow your logic... Invalid input."
		print "\t\tTry again, {0}".format(user)
		print "\nIs the GM Coregistration ok?"
		GM_CoReg=raw_input("Enter 0=Yes ; 1=NO ; or 9=Check: ").lower()
	##########################	
	if GM_CoReg in yes:
		GM_CoReg='0'
	elif GM_CoReg in no:
		GM_CoReg='1'
	elif GM_CoReg in check:
		GM_CoReg='9'
	##########################
	GM_CoRegNote=raw_input("\tAny comments on GM coreg to add?: ").lower()
	GM_CoRegNote=GM_CoRegNote.replace(',',' ')
	#Append commas for csv
	GM_GB=GM_GB+','
	GM_GBNote=GM_GBNote+' ,'
	GM_CoReg=GM_CoReg+','
	GM_CoRegNote=GM_CoRegNote+' ,'
	if '9' in GM_GB:
		GM_GB='False,'
	if '9' in GM_CoReg:
		GM_CoReg='False,'
	logGM=GM_GB+GM_GBNote+GM_CoReg+GM_CoRegNote
	return logGM
#################################################################################
# **Check faces displays the preprocessed whole-brain faces fMRI image 'swau*'  #
#################################################################################
def check_faces():
	print "\n#################################"
	print "##  :)  Check Faces fMRI  :)  ###"
	print "#################################"
	for file in os.listdir('.'):
		if fnmatch(file,'swau*'):
			os.system('afni -dset '+file+' &>/dev/null')	
	print "\nIs the Faces EPI Signal ok?" 
	print "+++++++++++++++++++++++++++++++"	   
	faceGB=raw_input("Enter 0=Yes ; 1=NO ; or 9=Check: ").lower()
	############################
	## Check Input for errors ##
	############################
	while faceGB not in yes+no+check:
		print "\nI don't follow your logic... Invalid input."
		print "\t\tTry again, {0}".format(user)
		print "\nIs the Faces EPI Signal ok?"			
		faceGB=raw_input("Enter 0=Yes ; 1=NO ; or 9=Check: ").lower()
	##########################
	if faceGB in yes:
		faceGB='0'
	elif faceGB in no:
		faceGB='1'
	elif faceGB in check:
		faceGB='9'
	###############################################################
	faceGBNote=raw_input("\tAny comments on face signal to add?: ")
	faceGBNote=faceGBNote.replace(',',' ')
	###############################################################
	print "\nCheck Faces EPI Coregistration"
	for file in os.listdir('.'):
		if fnmatch(file,'swau*'):
			os.system('afni -dset ~/abin/MNI152_T1_2009c+tlrc.BRIK '+file+' &>/dev/null')	
	print "\nIs the Faces EPI Coregistration ok?" 
	print "+++++++++++++++++++++++++++++++++++"	   
	faceCoReg=raw_input("Enter 0=Yes ; 1=NO ; or 9=Check: ").lower()
	############################
	## Check Input for errors ##
	############################
	while faceCoReg not in yes+no+check:
		print "\nI don't follow your logic... Invalid input."
		print "\t\tTry again, {0}".format(user)	
		print "\nIs the Faces EPI Coregistration ok?"			  
		faceCoReg=raw_input("Enter 0=Yes ; 1=NO ; or 9=Check: ").lower()
	#############################
	if faceCoReg in yes:
		faceCoReg='0'
	elif faceCoReg in no:
		faceCoReg='1'
	elif faceCoReg in check:
		faceCoReg='9'		
	##########################
	faceCoRegNote=raw_input("\tAny comments on face coreg to add?: ")
	faceCoRegNote=faceCoRegNote.replace(',',' ')
	#Append commas for csv
	faceGB=faceGB+','
	faceGBNote=faceGBNote+','
	faceCoReg=faceCoReg+','
	faceCoRegNote=faceCoRegNote+','
	if '9' in faceGB:
		faceGB='False,'
	if '9' in faceCoReg:
		faceCoReg='False,'
	logfaces=faceGB+faceGBNote+faceCoReg+faceCoRegNote
	return logfaces	
#############################################################################
# **Check MID displays the preprocessed whole-brain MID fMRI image 'swau*'  #
#############################################################################
def check_MID():
	print "\n###############################"
	print "##  $$  Check MID fMRI  $$   ##"
	print "###############################"
	for file in os.listdir('.'):
		if fnmatch(file,'swau*'):
			os.system('afni -dset '+file+' &>/dev/null')	
	print "\nIs the MID EPI Signal ok?" 
	print "+++++++++++++++++++++++++++++++++++"		   
	MIDGB=raw_input("Enter 0=Yes ; 1=NO ; or 9=Check: ").lower()
	############################
	## Check Input for errors ##
	############################
	while MIDGB not in yes+no+check:
		print "\nI don't follow your logic... Invalid input."
		print "\t\tTry again, {0}".format(user)
		print "\nIs the MID EPI Signal ok?" 
		MIDGB=raw_input("Enter 0=Yes ; 1=NO ; or 9=Check: ").lower()
	##########################
	if MIDGB in yes:
		MIDGB='0'
	elif MIDGB in no:
		MIDGB='1'
	elif MIDGB in check:
		MIDGB='9'
	##############################################################
	MIDGBNote=raw_input("\tAny comments on MID signal to add?: ")
	MIDGBNote=MIDGBNote.replace(',',' ')
	#############################################################
	print "\nCheck MID EPI Coregistration"
	for file in os.listdir('.'):
		if fnmatch(file,'swau*'):
			os.system('afni -dset ~/abin/MNI152_T1_2009c+tlrc.BRIK '+file+' &>/dev/null')
	print "\nIs the MID EPI Coregistration ok?" 
	print "+++++++++++++++++++++++++++++++"		   
	MIDCoReg=raw_input("Enter 0=Yes ; 1=NO ; or 9=Check: ").lower()
	############################
	## Check Input for errors ##
	############################
	while MIDCoReg not in yes+no+check:
		print "\nI don't follow your logic. Invalid input."
		print "Try again, {0}".format(user)	
		print "Is the MID EPI Coregistration ok?" 
		MIDCoReg=raw_input("Enter 0=Yes ; 1=NO ; or 9=Check: ").lower()
	MIDCoRegNote=raw_input("\tAny comments on MID coreg to add?: ")
	MIDCoRegNote=MIDCoRegNote.replace(',',' ')
	############################
	if MIDCoReg in yes:
		MIDCoReg='0'
	elif MIDCoReg in no:
		MIDCoReg='1'
	elif MIDCoReg in check:
		MIDCoReg='9'
	############################		
	#Append commas for csv
	MIDGB=MIDGB+','
	MIDGBNote=MIDGBNote+','
	MIDCoReg=MIDCoReg+','
	MIDCoRegNote=MIDCoRegNote+','
	if '9' in MIDGB:
		MIDGB='False,'
	if '9' in MIDCoReg:
		MIDCoReg='False,'
	logMID=MIDGB+MIDGBNote+MIDCoReg+MIDCoRegNote
	return logMID
####################################################################################
# **Check SS displays the preprocessed whole-brain stop signal fMRI image 'swau*'  #
####################################################################################
def check_ss():
	print "\n###################################"
	print "# <0-x-x> Check StopSignal fMRI ##"
	print "##################################"	
	for file in os.listdir('.'):
		if fnmatch(file,'swau*'):
			os.system('afni -dset '+file+' &>/dev/null')
	print "Is the Stop Signal EPI Signal ok?" 
	print "+++++++++++++++++++++++++++++++++++"							   
	ssGB=raw_input("Enter 0=Yes ; 1=NO ; or 9=Check: ").lower()
	############################
	## Check Input for errors ##
	############################
	while ssGB not in yes+no+check:
		print "\nI don't follow your logic... Invalid input."
		print "\t\tTry again, {0}".format(user)
		print "\nIs the Stop Signal EPI Signal ok?"		 	
		ssGB=raw_input("Enter 0=Yes ; 1=NO ; or 9=Check: ").lower()
	############################
	if ssGB in yes:
		ssGB='0'
	elif ssGB in no:
		ssGB='1'
	elif ssGB in check:
		ssGB='9'
	###########################################################
	ssGBNote=raw_input("\tAny comments on SS signal to add?: ")
	ssGBNote=ssGBNote.replace(',',' ')
	###########################################################
	print "\nCheck Stop Signal EPI Coregistration"
	for file in os.listdir('.'):
		if fnmatch(file,'swau*'):
			os.system('afni -dset ~/abin/MNI152_T1_2009c+tlrc.BRIK '+file+' &>/dev/null')
	print "+++++++++++++++++++++++++++++++++++"										   
	print "Is the Stop Signal EPI Coregistration ok?" 
	ssCoReg=raw_input("Enter 0=Yes ; 1=NO ; or 9=Check: ").lower()
	############################
	## Check Input for errors ##
	############################
	while ssCoReg not in yes+no+check:
		print "\nI don't follow your logic... Invalid input."
		print "\t\tTry again, {0}".format(user)
		print "\nIs the Sto Signal EPI Coregistration ok?"		 	
		ssCoReg=raw_input("Enter 0=Yes ; 1=NO ; or 9=Check: ")
	############################		
	if ssCoReg in yes:
		ssCoReg='0'
	elif ssCoReg in no:
		ssCoReg='1'
	elif ssCoReg in check:
		ssCoReg='9'
	##############################################################
	ssCoRegNote=raw_input("\tAny comments on SS coreg to add?: ")
	ssCoRegNote=ssCoRegNote.replace(',',' ')
	###############################################################
	#Append commas for csv
	ssGB=ssGB+','
	ssCoReg=ssCoReg+','
	ssGBNote=ssGBNote+','
	ssCoRegNote=ssCoRegNote+','
	if '9' in ssGB:
		ssGB='False,'
	if '9' in ssCoReg:
		ssCoReg='False,'
	logSS=ssGB+ssGBNote+ssCoReg+ssCoRegNote
	return logSS
#######################################################################################
# This function concatenates all responses to be logged in a single row in the CSV file
#######################################################################################
def log_answers(logfile,
				user,
				date,
				hotsub,
				loganat,
				logGM,
				logfaces,
				logMID,
				logSS,
				Comments
				):
	with open(logfile,'a') as f:
		f.writelines(['\n'+user+',',
				date+',',
				hotsub+',',
				loganat,
				logGM,
				logfaces,
				logMID,
				logSS,
				Comments])
		f.close()
	print "Saving Your Answers to CSV File"
	if path2backup in logfile:
		print "\t++Saving a backup to the server++ ...For your health"
	print "\nThank You So Much, {0}".format(user)*2
	return
##########################################################################################
###################        User interactions begin here           ########################
##########################################################################################
#Get username
user=raw_input("Please tell me your name: ")
#
print "\nHello {0}, I'm happy we're working together".format(user)
print "\nQC is a very important step in fMRI Analysis\n"
#
#Get subject to start QC with
print "\nLet's figure out where we left off...\n"
#	
#Marker to keep going after sub finished
go=True
print "\n~*~*~ Let the QC BEGIN ~*~*~\n"
##############################################
######## Running Code Starts Here ############
##############################################
while go:
	os.chdir(workdir)
	#####################################################################################
	#Find subject to work on, aka 'hotsub'
	hotsub=genfromtxt('hotsub.txt',dtype='str')
	#Get rid of numpy array format for printing and writing 
	hotsub=str(hotsub)
	#####################################################################################
	print "You are working on subject: {0}".format(hotsub)
	#Give subject index out of full list of subject
	print "Subject index: "+str(argwhere(allsubs==hotsub)[0][0])+" out of "+str(len(allsubs))
	print "\nHere we go...\n"
	#####################################################################################
	start=time.time()
	###################################
	######## Do Anats First ###########
	###################################
	try:
		os.chdir(path2anat+hotsub)
		loganat=check_anat()
	except OSError:
		print "\n***Cant Find Anatomical Image***\n"*2
		loganat='NoData,'*2
	#Try loading GM
	try:
		os.chdir(path2anat+hotsub)
		logGM=check_GM()
	except OSError:
		print "\n***Cant Find GM***\n"*2
		logGM='NoData,'*4
	###################################
	######## Do Tasks Next ############
	###################################
	print "\n\t**Working on Task fMRI**"
	#Try loading  Faces
	try:
		os.chdir(path2fmri+hotsub+'/EPI_faces/')
		logfaces=check_faces()
	except OSError:
		if "EPI_faces" not in os.listdir(path2fmri+hotsub):
			print "\n***Cant Find EPI faces data***\n"
			logfaces='NoData,'*4
	#Try loading  MID
	try:
		os.chdir(path2fmri+hotsub+'/EPI_short_MID/')
		logMID=check_MID()
	except OSError:
		if "EPI_short_MID" not in os.listdir(path2fmri+hotsub):
			print "\n***Cant Find EPI MID data***\n"
			logMID='NoData,'*4
	#Try loading SST
	try:
		os.chdir(path2fmri+hotsub+'/EPI_stop_signal/')
		logSS=check_ss()
	except OSError:
		if "EPI_stop_signal" not in os.listdir(path2fmri+hotsub):
			print "\n***Cant Find EPI stop data***\n"
			logSS='NoData,'*4
	################################
	######## Tasks Done ############
	################################			
	#Ask for Final Comments
	Comments=raw_input("\n***Any overall comments to make?***: ")
	Comments=Comments.replace(',',' ')
	#####################################################################
	############# SEND ALL USER INPUTS TO TERMINAL WINDOW ###############
	#####################################################################
	print "############################"
	print "### REVIEW YOUR ANSWERS-- ##"
	print "############################"
	if loganat.split(',')[0]=='1':
		print "Anatomical is: BAD"
	elif loganat.split(',')[0]=='0':
		print "Anatomical is: GOOD"
	elif loganat.split(',')[0]=='False':
		print "Anatomical is: to be checked later..."
	elif loganat.split(',')[0]=='NoData':
		print "Anatomical is: Missing Data"
	else:
		print "\nERROR! No anatomical feedback received"
		print "Go back and start over!\n"*4
	#GM---
	if logGM.split(',')[0]=='1':
		print "Gray Matter segmentation is: BAD"
	elif logGM.split(',')[0]=='0':
		print "Gray Matter segmentation is: GOOD"
	elif logGM.split(',')[0]=='False':
		print "Gray Matter segmentation is: to be checked later..."
	elif logGM.split(',')[0]=='NoData':
		print "Gray Matter is: Missing Data"		
	else:
		print "\nERROR! No GM segmentaiton feedback received"
		print "Go back and start over!\n"*4
	#GM---
	if logGM.split(',')[2]=='1':
		print "Gray Matter coregistration is: BAD"
	elif logGM.split(',')[2]=='0':
		print "Gray Matter coregistration is: GOOD"
	elif logGM.split(',')[2]=='False':
		print "Gray Matter coregistration is: to be checked later..."
	elif logGM.split(',')[2]=='NoData':
		print "Gray Matter is: Missing Data"		
	else:
		print "\nERROR! No GM coregistration feedback received"
		print "Go back and start over!\n"*4
	#FACES----
	if logfaces.split(',')[0]=='1':
		print "Faces data is: BAD"
	elif logfaces.split(',')[0]=='0':
		print "Faces data is: GOOD"
	elif logfaces.split(',')[0]=='False':
		print "Faces data is: to be checked later..."
	elif logfaces.split(',')[0]=='NoData':
		print "Faces data is: MISSING..."				
	else:
		print "\nERROR! No Faces data check feedback received"
		print "Go back and start over!\n"*4
	#FACES----
	if logfaces.split(',')[2]=='1':
		print "Faces coregistration is: BAD"
	elif logfaces.split(',')[2]=='0':
		print "Faces coregistration is: GOOD"
	elif logfaces.split(',')[2]=='False':
		print "Faces coregistration is: to be checked later..."
	elif logfaces.split(',')[2]=='NoData':
		print "Faces data is: MISSING..."		
	else:
		print "\nERROR! No Faces coregistration feedback received"
		print "Go back and start over!\n"*4
	#MID---
	if logMID.split(',')[0]=='1':
		print "MID data is: BAD"
	elif logMID.split(',')[0]=='0':
		print "MID data is: GOOD"
	elif logMID.split(',')[0]=='False':
		print "MID data is: to be checked later..."
	elif logMID.split(',')[0]=='NoData':
		print "MID data is: MISSING..."				
	else:
		print "\nERROR! No MID data check feedback received"
		print "Go back and start over!\n"*4
	#MID----
	if logMID.split(',')[2]=='1':
		print "MID coregistration is: BAD"
	elif logMID.split(',')[2]=='0':
		print "MID coregistration is: GOOD"
	elif logMID.split(',')[2]=='False':
		print "MID coregistration is: to be checked later..."
	elif logMID.split(',')[2]=='NoData':
		print "MID data is: MISSING..."			
	else:
		print "\nERROR! No MID coregistration feedback received"
		print "Go back and start over!\n"*4
	#STOP---
	if logSS.split(',')[0]=='1':
		print "SS data is: BAD"
	elif logSS.split(',')[0]=='0':
		print "SS data is: GOOD"
	elif logSS.split(',')[0]=='False':
		print "Stop Signal data is: to be checked later..."
	elif logSS.split(',')[0]=='NoData':
		print "Stop Signal data is: MISSING..."			
	else:
		print "\nERROR! No SS data check feedback received"
		print "Go back and start over!\n"*4
	#STOP---
	if logSS.split(',')[2]=='1':
		print "Stop Signal coregistration is: BAD"
	elif logSS.split(',')[2]=='0':
		print "Stop Signal coregistration is: GOOD"
	elif logSS.split(',')[2]=='False':
		print "Stop Signal coregistration is: to be checked later..."
	elif logSS.split(',')[2]=='NoData':
		print "Stop Signal data is: MISSING..."			
	else:
		print "\nERROR! Stop Signal coregistration feedback received"
		print "Go back and start over!\n"*4
	print '\n'
	print "Your overall comments were: "
	print '\t'+Comments	
	print "############################"
	print "### REVIEW YOUR ANSWERS ^ ##"
	print "############################"
	##################################
	####### Ask To log entries #######
	##################################
	ask2log=raw_input("\nShall I log your entries?: ").lower()
	while ask2log not in yes+no:
		print "\nI don't follow your logic... Invalid input."
		print "\t\tTry again, {0}".format(user)
		ask2log=raw_input("\nShall I log your entries?: ").lower()
	if ask2log in yes:
		#Log responses to csv, first locally "workdir", then again to backup directory
		log_answers(workdir+logfile,
					user,
					datetime.datetime.today().strftime('%m-%d-%Y'),
					hotsub,
					loganat,logGM,
					logfaces,logMID,logSS,
					Comments)
		###############################################
		log_answers(path2backup+logfile,
					user,
					datetime.datetime.today().strftime('%m-%d-%Y'),
					hotsub,
					loganat,logGM,
					logfaces,logMID,logSS,
					Comments)
		##################################################################################
		end=time.time()
		print "Time elpased QC'ing subject {0}:    {1} mins".format(hotsub,str((end-start)/60))
		##################################################################################
		#Change hotsub to the next one by going to the current index+1
		with open(workdir+'hotsub.txt','w') as f:
			f.write(str(allsubs[argwhere(allsubs==hotsub)+1]).strip("[[]]'"))
			f.close()
		#Change hotsub on server as a backup
		with open(path2backup+'hotsub.txt','w') as f:
			f.write(str(allsubs[argwhere(allsubs==hotsub)+1]).strip("[[]]'"))
			f.close()		 
		##################################################################################
		ask2continue=raw_input("\nWant to go to the next subject?: ").lower()
		while ask2continue not in yes+no:
			print "\nI don't follow your logic... Invalid input."
			print "\t\tTry again, {0}".format(user)
			ask2continue=raw_input("\nWant to go to the next subject?: ").lower()
		if ask2continue in yes:
			go=True
		else:
			print "\nOk Bye Bye {0}".format(user)
			print "I look forward to QC'ing with you again"
			go=False
	else:
		print "\nANSWERS NOT SAVED"
		print "\nGo Back And Start Again"*2
		go=False
		end=time.time()
		print "Time elapsed: {0} mins".format(str((end-start)/60))
os.chdir(workdir)