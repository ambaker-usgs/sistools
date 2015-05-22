#!/usr/bin/env python

###################################################################################################
#datalesstools.py
#By Adam Baker
#
#This program returns the dataless for a given network or station
###################################################################################################

#imports
import sys
from obspy.xseed import Parser

#variables
datalessPath = '/APPS/metadata/SEED/'

#functions
def getDataless(netsta):
	#the function that returns the dataless
	net = netsta[:2].upper()
	parsedDataless = Parser(datalessPath + net + '.dataless')
	return parsedDataless