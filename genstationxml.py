#!/usr/bin/env python

###################################################################################################
#genstationxml.py
#By Adam Baker
#
#This program generates Station XML for the purposes of SIS (http://anss-sis.scsn.org/sistest/)
###################################################################################################

import argparse
import blockettetools
import commands
import datalesstools
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

now = UTCDateTime.now()

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
	processChannels(dataless)
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
	isOpenStationEpoch = False
	for blockette in dataless:
		if blockette.id == 50 and blockette.start_effective_date <= now <= blockette.end_effective_date:
			preamble = ['<?xml version="1.0" ?>','<fsx:FDSNStationXML xsi:type="sis:RootType" schemaVersion="2.0" sis:schemaLocation="http://anss-sis.scsn.org/xml/ext-stationxml/2.0 http://anss-sis.scsn.org/xml/ext-stationxml/2.0/sis_extension.xsd" xmlns:fsx="http://www.fdsn.org/xml/station/1" xmlns:sis="http://anss-sis.scsn.org/xml/ext-stationxml/2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">']
			appendToFile(0, preamble)
			appendToFile(1, ['<fsx:Source>' + sisinfo.source() + '</fsx:Source>'])
			appendToFile(1, ['<fsx:Sender>' + sisinfo.sender() + '</fsx:Sender>'])
			appendToFile(1, ['<fsx:Created>' + str(UTCDateTime(now)) + '</fsx:Created>'])
			appendToFile(1, ['<fsx:Network code="' + blockette.network_code + '">'])
			network, description, netstaCount = fetchLegendEntry().split('|')
			appendToFile(2, ['<fsx:Description>' + description + '</fsx:Description>'])
			appendToFile(2, ['<fsx:TotalNumberStations>' + netstaCount + '</fsx:TotalNumberStations>'])
			appendToFile(2, ['<fsx:SelectedNumberStations>1</fsx:SelectedNumberStations>'])
			appendToFile(2, ['<fsx:Station xsi:type="sis:StationType" code="' + blockette.station_call_letters + '" startDate="' + stationStartDate(dataless) + '">'])
			processStationComments(dataless)
			appendToFile(3, ['<fsx:Latitude>' + str(blockette.latitude) + '</fsx:Latitude>'])
			appendToFile(3, ['<fsx:Longitude>' + str(blockette.longitude) + '</fsx:Longitude>'])
			appendToFile(3, ['<fsx:Elevation>' + str(blockette.elevation) + '</fsx:Elevation>'])
			network, station, name, description, town, region = fetchNetStaInfo(blockette).split('|')
			appendToFile(3, ['<fsx:Site>'])
			appendToFile(4, ['<fsx:Name>' + name + '</fsx:Name>'])
			appendToFile(4, ['<fsx:Description>' + description + '</fsx:Description>'])
			appendToFile(4, ['<fsx:Town>' + town + '</fsx:Town>'])
			appendToFile(4, ['<fsx:Region>' + region + '</fsx:Region>'])
			appendToFile(3, ['</fsx:Site>'])
			appendToFile(3, ['<fsx:Operator>'])
			appendToFile(4, ['<fsx:Agency>' + sisinfo.agency() + '</fsx:Agency>'])
			appendToFile(3, ['</fsx:Operator>'])
			appendToFile(3, ['<fsx:CreationDate>' + stationStartDate(dataless) + '</fsx:CreationDate>'])
			appendToFile(3, ['<fsx:TotalNumberChannels>' + str(blockette.number_of_channels) + '</fsx:TotalNumberChannels>'])
			appendToFile(3, ['<fsx:SelectedNumberChannels>' + selectedNumberChannels(dataless) + '</fsx:SelectedNumberChannels>'])

def stationStartDate(dataless):
	#returns the earliest start_effective_date
	startDates = []
	for blockette in dataless:
		if blockette.id == 50:
			startDates.append(blockette.start_effective_date)
	return str(min(startDates))

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

def fetchNetStaInfo(blkt):
	#fetches the info required for the Site tag
	fob = open('netstainfo.txt', 'r')
	contents = fob.read().split('\n')
	fob.close()
	for entry in contents:
		if blkt.network_code and blkt.station_call_letters in entry:
			return entry

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

def processStationComments(blockettes):
	#Writes the channel comments (blockette 59, if any) to the xml
	for blockette in blockettes:
		if blockette.id == 51:
			appendToFile(3, ['<fsx:Comment>'])
			appendToFile(4, ['<fsx:Value>' + fetchComment(dictB031, blockette.comment_code_key)[0] + '</fsx:Value>'])
			appendToFile(4, ['<fsx:BeginEffectiveTime>' + str(blockette.beginning_effective_time) +  '</fsx:BeginEffectiveTime>'])
			appendToFile(4, ['<fsx:EndEffectiveTime>' + str(blockette.end_effective_time) + '</fsx:EndEffectiveTime>'])
			appendToFile(4, ['<fsx:Author>'])
			appendToFile(5, ['<fsx:Name>' + 'USGS ASL RDSEED' + '</fsx:Name>'])
			appendToFile(4, ['</fsx:Author>'])
			appendToFile(3, ['</fsx:Comment>'])

def selectedNumberChannels(dataless):
	channelCount = 0
	for blockette in dataless:
		if blockette.id == 52 and blockette.start_date <= now <= blockette.end_date:
			channelCount += 1
	return str(channelCount)

def processChannels(dataless):
	netsta = net + sta
	channels = blockettetools.getChannels(dataless, now)
	for channel in channels:
		for blockette in channel:			
			if blockette.id == 52:
				appendToFile(3, ['<fsx:Channel xsi:type="sis:ChannelType" code="' + blockette.channel_identifier + '" startDate="' + str(blockette.start_date).split('.')[0] + '" endDate="' + str(blockette.end_date).split('.')[0] + '" locationCode="' + blockette.location_identifier + '">'])
				processChannelComments(channel)
				appendToFile(4, ['<fsx:Latitude>' + str(blockette.latitude) + '</fsx:Latitude>'])
				appendToFile(4, ['<fsx:Longitude>' + str(blockette.longitude) + '</fsx:Longitude>'])
				appendToFile(4, ['<fsx:Elevation>' + str(blockette.elevation) + '</fsx:Elevation>'])
				appendToFile(4, ['<fsx:Depth>' + str(blockette.local_depth) + '</fsx:Depth>'])
				appendToFile(4, ['<fsx:Azimuth>' + str(blockette.azimuth) + '</fsx:Azimuth>'])
				appendToFile(4, ['<fsx:Dip>' + str(blockette.dip) + '</fsx:Dip>'])
				processChannelFlags(blockette.channel_flags)
				appendToFile(4, ['<fsx:SampleRate>' + value2SciNo(blockette.sample_rate) + '</fsx:SampleRate>'])
				appendToFile(4, ['<fsx:ClockDrift>' + value2SciNo(blockette.max_clock_drift) + '</fsx:ClockDrift>'])
				appendToFile(4, ['<fsx:CalibrationUnits>'])
				appendToFile(5, ['<fsx:Name>' + fetchUnit(dictB034, blockette.units_of_calibration_input)[0] + '</fsx:Name>'])
				appendToFile(5, ['<fsx:Description>' + fetchUnit(dictB034, blockette.units_of_calibration_input)[1] + '</fsx:Description>'])
				appendToFile(4, ['</fsx:CalibrationUnits>'])
		if channelWithoutB062(channel):
			for blockette in channel:
				if blockette.id == 58 and blockette.stage_sequence_number == 0:
					appendToFile(4, ['<fsx:Response xsi:type="sis:ResponseType">'])
					appendToFile(5, ['<fsx:InstrumentSensitivity>'])
					appendToFile(6, ['<fsx:Value>' + value2SciNo(blockette.sensitivity_gain) + '</fsx:Value>'])
					appendToFile(6, ['<fsx:Frequency>' + value2SciNo(blockette.frequency) + '</fsx:Frequency>'])
			for blockette in channel:
				if blockette.id == 52:
					appendToFile(6, ['<fsx:InputUnits>'])
					appendToFile(7, ['<fsx:Name>' + fetchUnit(dictB034, blockette.units_of_signal_response)[0] + '</fsx:Name>'])
					appendToFile(7, ['<fsx:Description>' + fetchUnit(dictB034, blockette.units_of_signal_response)[1] + '</fsx:Description>'])
					appendToFile(6, ['</fsx:InputUnits>'])
				if blockette.id == 54 and blockette.stage_sequence_number == 2:
					appendToFile(6, ['<fsx:OutputUnits>'])
					appendToFile(7, ['<fsx:Name>' + fetchUnit(dictB034, blockette.signal_output_units)[0] + '</fsx:Name>'])
					appendToFile(7, ['<fsx:Description>' + fetchUnit(dictB034, blockette.signal_output_units)[1] + '</fsx:Description>'])
					appendToFile(6, ['</fsx:OutputUnits>'])
					appendToFile(5, ['</fsx:InstrumentSensitivity>'])
			appendToFile(4, ['</fsx:Response>'])
			appendToFile(3, ['</fsx:Channel>'])
			
			
			# if blockette.id == 53:
			# 	appendToFile(4, ['<sis:SubResponse sequenceNumber="1">'])
			# 	appendToFile(5, ['<sis:EquipmentLink>'])
			# 	appendToFile(6, ['<sis:SerialNumber>' + '#####' + '</sis:SerialNumber>'])
			# 	appendToFile(6, ['<sis:ModelName>' + 'model name (sensor)' + '</sis:ModelName>'])
			# 	appendToFile(6, ['<sis:Category>' + 'category' + '</sis:Category>'])
			# 	appendToFile(6, ['<sis:ComponentName>' + '1/2/Z' + '</sis:ComponentName>'])
			# 	appendToFile(6, ['<sis:CalibrationDate>' + 'YYYY-MM-DDTHH:MM:SSZ' + '</sis:CalibrationDate>'])
			# 	appendToFile(5, ['</sis:EquipmentLink>'])
			# 	appendToFile(4, ['</sis:Subresponse>'])
			# 	appendToFile(4, ['<sis:SubResponse sequenceNumber="2">'])
			# 	appendToFile(5, ['<sis:EquipmentLink>'])
			# 	appendToFile(6, ['<sis:SerialNumber>' + 'str(#####)' + '</sis:SerialNumber>'])
			# 	appendToFile(6, ['<sis:ModelName>' + 'model name (datalogger)' + '</sis:ModelName>'])
			# 	appendToFile(6, ['<sis:Category>' + 'category' + '</sis:Category>'])
			# 	appendToFile(6, ['<sis:ComponentName>' + 'DATA1' + '</sis:ComponentName>'])
			# 	appendToFile(6, ['<sis:CalibrationDate>' + 'YYYY-MM-DDTHH:MM:SSZ' + '</sis:CalibrationDate>'])
			# 	appendToFile(5, ['</sis:EquipmentLink>'])
			# 	appendToFile(5, ['<sis:PreampGain>' + 'str(######)' + '</sis:PreampGain>'])
			# 	appendToFile(4, ['</sis:Subresponse>'])
			# 	appendToFile(4, ['<sis:SubResponse sequenceNumber="3">'])
			# 	appendToFile(5, ['<sis:ResponseDictLink>'])
			# 	appendToFile(6, ['<sis:Name>' + 'name' + '</sis:Name>'])
			# 	appendToFile(6, ['<sis:SISNameSpace>' + sisinfo.agency() + '</sis:SISNameSpace>'])
			# 	appendToFile(6, ['<sis:Type>' + 'type (filter sequence)' + '</sis:Type>'])
			# 	appendToFile(5, ['</sis:ResponseDictLink>'])
			# 	appendToFile(4, ['</sis:Subresponse>'])
			# 	appendToFile(3, ['</fsx:Response>'])
			# 	appendToFile(3, ['<sis:MeasurementType>' + 'measurement type' + '</sis:MeasurementType>'])
			# 	appendToFile(3, ['<sis:SignalUnis>'])
			# 	appendToFile(4, ['<sis:Name>' + 'u' + '</sis:Name>'])
			# 	appendToFile(4, ['<sis:Description>' + 'units' + '</sis:Description>'])
			# 	appendToFile(3, ['</sis:SignalUnits>'])
			# 	appendToFile(3, ['<sis:Clip>' + 'str(######)' + '</sis:Clip>'])
			# 	appendToFile(3, ['<sis:PinNumber>' + str(1) + '</sis:PinNumber>'])
			# 	appendToFile(3, ['<sis:ChannelSource>' + 'SEED' + '</sis:ChannelSource>'])

def getDictionaries(netsta):
	net = netsta[:2]
	sta = netsta[2:]
	b031, b033, b034 = parseRDSEEDAbbreviations(commands.getstatusoutput(formRDSEEDCommand(net, sta))[-1])
	return b031, b033, b034

def formRDSEEDCommand(net, sta):
	netsta = net + '_' + sta
	path = ''
	if os.path.exists('/xs0/seed/' + netsta):
		path = '/xs0/seed/' + netsta
	elif os.path.exists('/xs1/seed/' + netsta):
		path = '/xs1/seed/' + netsta
	else:
		print 'No station ' + netsta + ' found. Please check again.'
	path = globMostRecent(globMostRecent(path))
	if os.path.exists(path + '/00_LHZ.512.seed'):
		return 'rdseed -f ' + path + '/00_LHZ.512.seed -g /APPS/metadata/SEED/' + net.upper() + '.dataless -a'
	else:
		print 'No suitable channel found (fomRDSEEDCommand())'
	
def globMostRecent(filepath):
	paths = glob.glob(filepath + '/*')
	pathsTemp = []
	for path in paths:
		if len(path.split('/')[-1]) <= 16 and 'SAVE' not in path:
			pathsTemp.append(path)
	return max(pathsTemp)

def parseRDSEEDAbbreviations(output):
	b031 = []
	b033 = []
	b034 = []
	for group in output.split('#\t\t\n'):
		if 'B031' == group[:4]:
			dictionary = {}
			for line in group.strip().split('\n'):
				if 'B031F03' in line:
					dictionary['comment code id'] = int(line.split('  ')[-1].strip())
				elif 'B031F04' in line:
					dictionary['comment class code'] = line.split('  ')[-1].strip()
				elif 'B031F05' in line:
					dictionary['comment text'] = line.split('  ')[-1].strip()
				elif 'B031F06' in line:
					dictionary['comment units'] = line.split('  ')[-1].strip()
			b031.append(dictionary)
		elif 'B033' == group[:4]:
			dictionary = {}
			for line in group.strip().split('\n'):
				if 'B033F03' in line:
					dictionary['description key code'] = int(line.split('  ')[-1].strip())
				elif 'B033F04' in line:
					dictionary['abbreviation description'] = line.split('  ')[-1].strip()
			b033.append(dictionary)
		elif 'B034' == group[:4]:
			dictionary = {}
			for line in group.strip().split('\n'):
				if 'B034F03' in line:
					dictionary['unit code'] = int(line.split('  ')[-1].strip())
				elif 'B034F04' in line:
					dictionary['unit name'] = line.split('  ')[-1].strip()
				elif 'B034F05' in line:
					dictionary['unit description'] = line.split('  ')[-1].strip()
			b034.append(dictionary)
	return b031, b033, b034

def processChannelFlags(flags):
	for flag in blockettetools.describeChannelFlags(flags):
		appendToFile(4, ['<Type>' + flag.upper() + '</Type>'])

def fetchComment(dictB031, value):
	#blockette 31
	for comment in dictB031:
		if value == comment['comment code id']:
			return [comment['comment text'], comment['comment units'], comment['comment class code']]
	return ['No comments found', 'N/A', '0']

def fetchInstrument(dictB033, value):
	#blockette 33
	for instrument in dictB033:
		if value == instrument['description key code']:
			return instrument['abbreviation description']
	return 'No instrument found'

def fetchUnit(dictB034, value):
	#blockette 34
	for unit in dictB034:
		if value == unit['unit code']:
			return [unit['unit name'], unit['unit description']]
	return ['None', 'No units found']

def channelWithoutB062(channel):
	for blockette in channel:
		if blockette.id == 62:
			return False
	return True

def processOutro(dataless):
	# appendToFile(3, ['<sis:DatumVertical>' + 'WGS84' + '</sis:DatumVertical>'])
	appendToFile(2, ['</fsx:Station>'])
	appendToFile(1, ['</fsx:Network>'])
	appendToFile(0, ['</fsx:FDSNStationXML>'])

def value2SciNo(value):
	#converts the string, int, or float value into scientific notation, returns it as a string
	value = "%e" % float(value)
	# if value[0] != '-':
	# 	value = '+' + value
	return value.replace('e','E')

def processChannelComments(blockettes):
	#Writes the channel comments (blockette 59, if any) to the xml
	for blockette in blockettes:
		if blockette.id == 59:
			appendToFile(4, ['<fsx:Comment>'])
			appendToFile(5, ['<fsx:Value>' + fetchComment(dictB031, blockette.comment_code_key)[0] + '</fsx:Value>'])
			appendToFile(5, ['<fsx:BeginEffectiveTime>' + str(blockette.beginning_of_effective_time) +  '</fsx:BeginEffectiveTime>'])
			appendToFile(5, ['<fsx:EndEffectiveTime>' + str(blockette.end_effective_time) + '</fsx:EndEffectiveTime>'])
			appendToFile(5, ['<fsx:Author>'])
			appendToFile(6, ['<fsx:Name>' + 'USGS ASL RDSEED' + '</fsx:Name>'])
			appendToFile(5, ['</fsx:Author>'])
			appendToFile(4, ['</fsx:Comment>'])

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

dictB031, dictB033, dictB034 = getDictionaries(net + sta)

if isvalidnetsta.isValidNetSta(net, sta):
	processDataless(datalesstools.getStationDataless(net + sta))
else:
	print 'Network and station found to not be valid (isvalidnetsta.py)'

print 'Process lasted', int(now - (UTCDateTime.now())), 'seconds'