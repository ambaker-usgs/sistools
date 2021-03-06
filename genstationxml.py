#!/usr/bin/env python

###################################################################################################
#genstationxml.py
#By Adam Baker
#
#This program generates Station XML for the purposes of SIS (http://anss-sis.scsn.org/sistest/)
###################################################################################################

import argparse
import datalesstools
import datetime
import glob
import isvalidnetsta
import os
import sisinfo
import urllib2

from obspy.core import UTCDateTime

legendPath = 'networklegend.txt'
source = 'USGS/Albuquerque Seismological Laboratory'
indent = '\t'
debug = True

now = datetime.datetime.today()

def getArguments():
	#This function parses the command line arguments
	parser = argparse.ArgumentParser(description='Code to compare data availability')

	#Sets flag for the network
	parser.add_argument('-n', action = "store",dest="net", \
		default = "*", help="Network to check: NN", type = str, required = True)

	#Sets flag for the station (optional)
	parser.add_argument('-s', action = "store",dest="sta", \
		default = "*", help="Station to check: SSSS", type = str, required = True)

	#Sets flag for the output filename
	parser.add_argument('-o', action = "store",dest="outputFilename", \
		default = "*", help="Output filename: NN_SSSS.xml", type = str, required = False)

	parserval = parser.parse_args()
	return parserval

def parseNetworkDataless(parsedDataless):
	blockettes = [net]
	for station in parsedDataless.stations:
		for blockette in station:
			if blockette.id not in blockettes:
				blockettes.append(blockette.id)
	print blockettes

def parseStationDataless(parsedDataless):
	#allows for collection of the station's dataless over many epochs
	for station in parsedDataless.stations:
		for blockette in station:
			if blockette.id == 50:
				if blockette.station_call_letters == sta:
					return station
			else:
				break
	# for epoch in parsedStation:
		# print 'EPOCH STARTING'
		# for blockette in epoch:
			# if blockette.id == 50:
			# 	print blockette.start_effective_date, blockette.end_effective_date, blockette.latitude, blockette.longitude, blockette.elevation
			# elif blockette.id == 52:
			# 	print blockette.location_identifier, blockette.channel_identifier
			# if blockette.id not in blockettes:
			# 	blockettes.append(blockette.id)
	# print blockettes
			# if blockette.id == 50:
			# 	print blockette.station_call_letters, blockette.start_effective_date, blockette.end_effective_date
			# else:
			# 	break

def processDataless(dataless):
	initializeOutputFile()
	processIntro(dataless)
	processChannel(dataless)
	processOutro(dataless)

def initializeOutputFile():
	#initiates the output file in the network's directory
	if net not in glob.glob('*'):
		#checks to see if the directory exists; if not, it creates the directory
		os.system('mkdir ' + net)
		if debug:
			print 'creating directory', net
	if outputFilepath in glob.glob(net + '/*'):
		#checks to see if there already exists a file with the same name
		#if so, it renames it to *_old
		if os.path.isfile(outputFilepath + '_old'):
			#checks to see if there already exists a file with the suffix _old
			#if so, it removes the old one to create the new one
			if debug:
				print 'Erasing ' + outputFilepath + '_old from disk'
			os.system('rm ' + outputFilepath + '_old')
		if os.path.isfile(outputFilepath):
			if debug:
				print 'Renaming ' + outputFilepath + ' to ' + outputFilepath + '_old'
			os.system('mv ' + outputFilepath + ' ' + outputFilepath + '_old')
	if debug:
		print 'Initializing ' + outputFilepath
	fob = open(outputFilepath, 'w')
	fob.write('')
	fob.close()

def processIntro(dataless):
	#processes the start of the xml file, mostly dealing with blockette 50 of the dataless
	b50sd = []
	latitude = ''
	longitude = ''
	elevation = ''
	channelCount = ''
	preamble = ['<?xml version="1.0" ?>','<fsx:FDSNStationXML xsi:type="sis:RootType" schemaVersion="2.0" sis:schemaLocation="http://anss-sis.scsn.org/xml/ext-stationxml/2.0 http://anss-sis.scsn.org/xml/ext-stationxml/2.0/sis_extension.xsd" xmlns:fsx="http://www.fdsn.org/xml/station/1" xmlns:sis="http://anss-sis.scsn.org/xml/ext-stationxml/2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">']
	appendToFile(0, preamble)
	appendToFile(1, ['<fsx:Source>' + sisinfo.source() + '</fsx:Source>'])
	appendToFile(1, ['<fsx:Sender>' + sisinfo.sender() + '</fsx:Sender>'])
	appendToFile(1, ['<fsx:Created>' + str(now).replace(' ','T') + 'Z' + '</fsx:Created>'])
	appendToFile(1, ['<fsx:Network code="' + net + '">'])
	for blockette in dataless:
		if blockette.id == 50:
			if blockette.end_effective_date - UTCDateTime(now) > 0:
				#checks if the current station epoch is open, if so, set to True
				isOpenStationEpoch = True
			else:
				#if not, set to False. This prevents subsequent closed epochs from being written to xml
				isOpenStationEpoch = False
			if isOpenStationEpoch:
				if blockette.id == 50:
					b50sd.append(blockette.start_effective_date)
					latitude = str(blockette.latitude)
					longitude = str(blockette.longitude)
					elevation = str(blockette.elevation)
					channelCount = str(blockette.number_of_channels)
	network, description, netstaCount = fetchLegendEntry().split('|')
	appendToFile(2, ['<fsx:Description>' + description + '</fsx:Description>'])
	appendToFile(2, ['<fsx:TotalNumberStations>' + netstaCount + '</fsx:TotalNumberStations>'])
	appendToFile(2, ['<fsx:SelectedNumberStations>1</fsx:SelectedNumberStations>'])
	appendToFile(2, ['<fsx:Station xsi:type="sis:StationType" code="' + sta + '" startDate="' + str(min(b50sd)) + '">'])
	appendToFile(3, ['<fsx:Latitude>' + latitude + '</fsx:Latitude>'])
	appendToFile(3, ['<fsx:Longitude>' + longitude + '</fsx:Longitude>'])
	appendToFile(3, ['<fsx:Elevation>' + elevation + '</fsx:Elevation>'])
	appendToFile(3, ['<fsx:Site>'])
	appendToFile(4, ['<fsx:Name>' + '</fsx:Name>'])
	appendToFile(4, ['<fsx:Description>' + '</fsx:Description>'])
	appendToFile(4, ['<fsx:Town>' + '</fsx:Town>'])
	appendToFile(4, ['<fsx:Region>' + '</fsx:Region>'])
	appendToFile(3, ['</fsx:Site>'])
	appendToFile(3, ['<fsx:Operator>'])
	appendToFile(4, ['<fsx:Agency>' + sisinfo.agency() + '</fsx:Agency>'])
	appendToFile(3, ['</fsx:Operator>'])
	appendToFile(3, ['<fsx:CreationDate>' + str(min(b50sd)) + '</fsx:CreationDate>'])
	appendToFile(3, ['<fsx:TotalNumberChannels>' + channelCount + '</fsx:TotalNumberChannels>'])
	appendToFile(3, ['<fsx:SelectedNumberChannels>' + channelCount + '</fsx:SelectedNumberChannels>'])

def fetchLegendEntry():
	legendPath = 'networklegend.txt'
	if not legendAlreadyExists():
		response = urllib2.urlopen('http://ds.iris.edu/mda/' + net + '/')
		pageSource = response.read()
		description = pageSource.split('::')[1].strip()
		# stationCount = pageSource.split('network (')[1].split()[0]
		addLegendEntry(net, description, stationCount)
	return getLegendEntry()

def legendAlreadyExists():
	#checks networklegend.txt to see if the network already exists in the legend
	legend = readLegend()
	for entry in legend:
		if net == entry.split(' | ')[0] and len(net) > 0:
			return True
	return False

def readLegend():
	#reads networklegend.txt
	fob = open(legendPath, 'r')
	legend = fob.read().split('\n')
	fob.close()
	return legend

def getLegendEntry():
	#fetches the legend entry from networklegend.txt
	legend = readLegend()
	for entry in legend:
		if net in entry:
			return entry.strip()

def addLegendEntry(network, description, stationCount):
	#adds the legend entry to networklegend.txt
	fob = open(legendPath, 'a')
	fob.write(network + ' | ' + description + ' | ' + stationCount + '\n')
	fob.close()

def appendToFile(tabCount, contents):
	#writes the contents given to file and indents it accordingly
	fob = open(outputFilepath, 'a')
	for index in range(len(contents)):
		line = contents[index]
		fob.write(indent * tabCount + line + '\n')
	fob.close()

def processChannel(dataless):
	#isOpenStationEpoch refers to having found the open epoch
	isOpenStationEpoch = False
	#processes and writes to file the channel xml to the output file
	for blockette in dataless:
		if blockette.id == 50:
			if blockette.end_effective_date - UTCDateTime(now) > 0:
				#checks if the current station epoch is open, if so, set to True
				isOpenStationEpoch = True
			else:
				#if not, set to False. This prevents subsequent closed epochs from being written to xml
				isOpenStationEpoch = False
		if isOpenStationEpoch:
			print blockette.id
			if blockette.id == 52:
				appendToFile(3, ['<fsx:Channel xsi:type="sis:ChannelType" code="' + blockette.channel_identifier + '" startDate="' + str(blockette.start_date) + '" locationCode="' + blockette.location_identifier + '">'])
				# appendToFile(3, ['<fsx:Comment>'])
				# appendToFile(4, ['<fsx:Value>' + '</fsx:Value>'])
				# appendToFile(4, ['<fsx:BeginEffectiveTime>' + '</fsx:BeginEffectiveTime>'])
				# appendToFile(4, ['<fsx:EndEffectiveTime>' + '</fsx:EndEffectiveTime>'])
				# appendToFile(4, ['<fsx:Author>'])
				# appendToFile(5, ['<fsx:Name>' + '</fsx:Name>'])
				# appendToFile(4, ['</fsx:Author>'])
				# appendToFile(3, ['</fsx:Comment>'])
				appendToFile(4, ['<fsx:Latitude>' + str(blockette.latitude) + '</fsx:Latitude>'])
				appendToFile(4, ['<fsx:Longitude>' + str(blockette.longitude) + '</fsx:Longitude>'])
				appendToFile(4, ['<fsx:Elevation>' + str(blockette.elevation) + '</fsx:Elevation>'])
				appendToFile(4, ['<fsx:Depth>' + str(blockette.local_depth) + '</fsx:Depth>'])
				appendToFile(4, ['<fsx:Azimuth>' + str(blockette.azimuth) + '</fsx:Azimuth>'])
				appendToFile(4, ['<fsx:Dip>' + str(blockette.dip) + '</fsx:Dip>'])
				appendToFile(4, ['<fsx:SampleRate>' + str(blockette.sample_rate) + '</fsx:SampleRate>'])
				appendToFile(4, ['<fsx:ClockDrift>' + str(blockette.max_clock_drift) + '</fsx:ClockDrift>'])
				# appendToFile(4, ['<fsx:CalibrationUnits>'])
				# appendToFile(5, ['<fsx:Name>' + 'A' + '</fsx:Name>'])
				# appendToFile(5, ['<fsx:Description>' + 'Amperes' + '</fsx:Description>'])
				# appendToFile(4, ['</fsx:CalibrationUnits>'])
			if blockette.id == 53:
				appendToFile(4, ['<fsx:Response xsi:type="sis:ResponseType">'])
				appendToFile(5, ['<fsx:InstrumentSensitivity>'])
				appendToFile(6, ['<fsx:Value>' + value2SciNo(blockette.A0_normalization_factor) + '</fsx:Value>'])
				appendToFile(6, ['<fsx:Frequency>' + value2SciNo(blockette.normalization_frequency) + '</fsx:Frequency>'])
				appendToFile(6, ['<fsx:InputUnits>'])
				appendToFile(7, ['<fsx:Name>' + 'm/s' + '</fsx:Name>'])
				appendToFile(7, ['<fsx:Description>' + 'meters per second' + '</fsx:Description>'])
				appendToFile(6, ['</fsx:InputUnits>'])
				appendToFile(6, ['<fsx:OutputUnits>'])
				appendToFile(7, ['<fsx:Name>' + 'counts' + '</fsx:Name>'])
				appendToFile(7, ['<fsx:Description>' + 'Digital counts' + '</fsx:Description>'])
				appendToFile(6, ['</fsx:OutputUnits>'])
				appendToFile(5, ['</fsx:InstrumentSensitivity>'])
				appendToFile(4, ['</fsx:Response>'])
				# appendToFile(5, ['<sis:SubResponse sequenceNumber="1">'])
				# appendToFile(6, ['<sis:EquipmentLink>'])
				# appendToFile(7, ['<sis:SerialNumber>' + '#####' + '</sis:SerialNumber>'])
				# appendToFile(7, ['<sis:ModelName>' + 'STS-2.5' + '</sis:ModelName>'])
				# appendToFile(7, ['<sis:Category>' + 'SENSOR' + '</sis:Category>'])
				# appendToFile(7, ['<sis:ComponentName>' + '1/2/Z' + '</sis:ComponentName>'])
				# appendToFile(7, ['<sis:CalibrationDate>' + 'YYYY-MM-DDTHH:MM:SSZ + '</sis:CalibrationDate>'])
				# appendToFile(6, ['</sis:EquipmentLink>'])
				# appendToFile(5, ['</sis:Subresponse>'])
				# appendToFile(5, ['<sis:SubResponse sequenceNumber="2">'])
				# appendToFile(6, ['<sis:EquipmentLink>'])
				# appendToFile(7, ['<sis:SerialNumber>' + str(#####) + '</sis:SerialNumber>'])
				# appendToFile(7, ['<sis:ModelName>' + 'Q330' + '</sis:ModelName>'])
				# appendToFile(7, ['<sis:Category>' + 'LOGGERBOARD' + '</sis:Category>'])
				# appendToFile(7, ['<sis:ComponentName>' + 'DATA1' + '</sis:ComponentName>'])
				# appendToFile(7, ['<sis:CalibrationDate>' + 'YYYY-MM-DDTHH:MM:SSZ + '</sis:CalibrationDate>'])
				# appendToFile(6, ['</sis:EquipmentLink>'])
				# appendToFile(6, ['<sis:PreampGain>' + str(######) + '</sis:PreampGain>'])
				# appendToFile(5, ['</sis:Subresponse>'])
				# appendToFile(5, ['<sis:SubResponse sequenceNumber="3">'])
				# appendToFile(6, ['<sis:ResponseDictLink>'])
				# appendToFile(7, ['<sis:Name>' + 'Q330.B100-40.MS' + '</sis:Name>'])
				# appendToFile(7, ['<sis:SISNameSpace>' + sisinfo.agency() + '</sis:SISNameSpace>'])
				# appendToFile(7, ['<sis:Type>' + 'SENSOR' + '</sis:Type>'])
				# appendToFile(6, ['</sis:ResponseDictLink>'])
				# appendToFile(5, ['</sis:Subresponse>'])
				# appendToFile(4, ['</sis:Response>'])
				# appendToFile(4, ['<sis:MeasurementType>' + 'VELOCITY_TRANSDUCER' + '</sis:MeasurementType>'])
				# appendToFile(4, ['<sis:SignalUnis>'])
				# appendToFile(5, ['<sis:Name>' + 'm/s' + '</sis:Name>'])
				# appendToFile(5, ['<sis:Description>' + 'meters per second' + '</sis:Description>'])
				# appendToFile(4, ['</sis:SignalUnits>'])
				# appendToFile(4, ['<sis:Clip>' + str(######) + '</sis:Clip>'])
				# appendToFile(4, ['<sis:PinNumber>' + str(1) + '</sis:PinNumber>'])
				# appendToFile(4, ['<sis:ChannelSource>' + 'SEED' + '</sis:ChannelSource>'])
			if blockette.id == 58:
				print '***', blockette.stage_sequence_number

def processOutro(dataless):
	appendToFile(3, ['<sis:DatumVertical>' + 'WGS84' + '</sis:DatumVertical>'])
	appendToFile(2, ['</fsx:Station>'])
	appendToFile(1, ['</fsx:Network>'])
	appendToFile(0, ['</fsx:FDSNStationXML>'])

def value2SciNo(value):
	#converts the string, int, or float value into scientific notation, returns it as a string
	value = "%e" % float(value)
	# if value[0] != '-':
	# 	value = '+' + value
	return value.replace('e','E')

#setting global variables
parserval = getArguments()
net = parserval.net.upper()
sta = parserval.sta.upper()
outputFilename = parserval.outputFilename
if outputFilename == '*':
	#if no custom filename is given, it defaults to NN_SSSS.xml
	outputFilename = net + '_' + sta + '.xml'
	if debug:
		print 'Your output file will be named ' + outputFilename
if '.xml' != outputFilename[-4:]:
	#appends a file extension if one isn't given
	if debug:
		print 'Output filename changed from ' + outputFilename + ' to ' + outputFilename + '.xml'
	outputFilename += '.xml'
outputFilepath = net + '/' + outputFilename

if isvalidnetsta.isValidNetSta(net, sta):
	datalessObj = parseStationDataless(datalesstools.getDataless(net + sta))
	processDataless(datalessObj)
else:
	print 'Network and station found to not be valid (isvalidnetsta.py)'

print 'Process lasted', (datetime.datetime.today() - now).seconds, 'seconds'