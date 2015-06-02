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
	#the function that returns the raw dataless
	net = netsta[:2].upper()
	parsedDataless = Parser(datalessPath + net + '.dataless')
	return parsedDataless

def getStationDataless(netsta):
	#the function that returns the dataless for a given station
	net = netsta[:2].upper()
	parsedDataless = Parser(datalessPath + net + '.dataless')
	if len(netsta) > 2:
		sta = netsta[2:].upper()
		for station in parsedDataless.stations:
			for blockette in station:
				if blockette.id == 50:
					if blockette.station_call_letters == sta:
						return station

def getNetworkDataless(netsta):
	#the function that returns the dataless for a given network
	net = netsta[:2].upper()
	parsedDataless = Parser(datalessPath + net + '.dataless')
	return parsedDataless.stations