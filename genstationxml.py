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
indent = '  '
debug = True

polynomialSupported = False

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
		if blockette.id == 50 and blockette.start_effective_date <= now <= validDate(blockette.end_effective_date):
			preamble = ['<?xml version="1.0" ?>','<fsx:FDSNStationXML xsi:type="sis:RootType" schemaVersion="2.0" sis:schemaLocation="http://anss-sis.scsn.org/xml/ext-stationxml/2.0 http://anss-sis.scsn.org/xml/ext-stationxml/2.0/sis_extension.xsd" xmlns:fsx="http://www.fdsn.org/xml/station/1" xmlns:sis="http://anss-sis.scsn.org/xml/ext-stationxml/2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">']
			appendToFile(0, preamble)
			appendToFile(1, ['<fsx:Source>' + sisinfo.source() + '</fsx:Source>'])
			appendToFile(1, ['<fsx:Sender>' + sisinfo.sender() + '</fsx:Sender>'])
			appendToFile(1, ['<fsx:Created>' + str(UTCDateTime(now)) + '</fsx:Created>'])
			network, description, netstaCount, startDate, endDate = fetchLegendEntry().split(' | ')
			appendToFile(1, ['<fsx:Network code="' + blockette.network_code + '" startDate="' + startDate + '" endDate="' + endDate + '">'])
			appendToFile(2, ['<fsx:Description>' + description + '</fsx:Description>'])
			appendToFile(2, ['<fsx:TotalNumberStations>' + netstaCount + '</fsx:TotalNumberStations>'])
			appendToFile(2, ['<fsx:SelectedNumberStations>1</fsx:SelectedNumberStations>'])
			appendToFile(2, ['<fsx:Station code="' + blockette.station_call_letters + '" startDate="' + stationStartDate(dataless) + '">'])
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
		startDate = str(UTCDateTime(int(pageSource.split('Start Year</TD><TD BGCOLOR="#FFFFFF">')[1][:4]),1,1)).split('.')[0]
		endDate = str(UTCDateTime(int(pageSource.split('End Year</TD><TD BGCOLOR="#DDFFEE">')[1][:4]),12,31,23,59,59)).split('.')[0]
		# stationCount = pageSource.split('network (')[1].split()[0]
		addLegendEntry(net, description, stationCount, startDate, endDate)
		
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
		if blkt.network_code and str(blkt.station_call_letters) in entry:
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
			appendToFile(4, ['<fsx:BeginEffectiveTime>' + str(validDate(blockette.beginning_effective_time)).split('.')[0] +  '</fsx:BeginEffectiveTime>'])
			appendToFile(4, ['<fsx:EndEffectiveTime>' + str(validDate(blockette.end_effective_time)).split('.')[0] + '</fsx:EndEffectiveTime>'])
			appendToFile(4, ['<fsx:Author>'])
			appendToFile(5, ['<fsx:Name>' + 'ASL RDSEED' + '</fsx:Name>'])
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
				appendToFile(3, ['<fsx:Channel locationCode="' + str(blockette.location_identifier) + '" startDate="' + str(blockette.start_date).split('.')[0] + '" endDate="' + str(validDate(blockette.end_date)).split('.')[0] + '" code="' + blockette.channel_identifier + '">'])
				processChannelComments(channel)
				appendToFile(4, ['<fsx:Latitude>' + str(blockette.latitude) + '</fsx:Latitude>'])
				appendToFile(4, ['<fsx:Longitude>' + str(blockette.longitude) + '</fsx:Longitude>'])
				appendToFile(4, ['<fsx:Elevation>' + str(blockette.elevation) + '</fsx:Elevation>'])
				appendToFile(4, ['<fsx:Depth>' + str(blockette.local_depth) + '</fsx:Depth>'])
				appendToFile(4, ['<fsx:Azimuth>' + str(blockette.azimuth) + '</fsx:Azimuth>'])
				appendToFile(4, ['<fsx:Dip>' + str(blockette.dip) + '</fsx:Dip>'])
				processChannelFlags(blockette.channel_flags)
				appendToFile(4, ['<fsx:SampleRate>' + str(blockette.sample_rate) + '</fsx:SampleRate>'])
				appendToFile(4, ['<fsx:ClockDrift>' + str(blockette.max_clock_drift) + '</fsx:ClockDrift>'])
				# appendToFile(4, ['<fsx:Sensor>'])
				# appendToFile(5, ['<fsx:Type>' + fetchInstrument(dictB033, blockette.instrument_identifier) + '</fsx:Type>'])
				# appendToFile(4, ['</fsx:Sensor>'])
				appendToFile(4, ['<fsx:Response xsi:type="sis:ResponseType">'])
				appendToFile(5, ['<fsx:InstrumentSensitivity>'])
				for blockette in channel:
					if blockette.id == 58 and blockette.stage_sequence_number == 0:
						appendToFile(6, ['<fsx:Value>' + value2SciNo(blockette.sensitivity_gain) + '</fsx:Value>'])
						appendToFile(6, ['<fsx:Frequency>' + value2SciNo(blockette.frequency) + '</fsx:Frequency>'])
				for blockette in channel:
					if blockette.id == 53:
						appendToFile(6, ['<fsx:InputUnits>'])
						appendToFile(7, ['<fsx:Name>' + fetchUnit(dictB034, blockette.stage_signal_input_units)[0] + '</fsx:Name>'])
						appendToFile(7, ['<fsx:Description>' + fetchUnit(dictB034, blockette.stage_signal_input_units)[1] + '</fsx:Description>'])
						appendToFile(6, ['</fsx:InputUnits>'])
						if noB054(channel):
							#in the event of no B054 in channel, proceed with the output units that SIS Parser (v2.0) requires
							appendToFile(6, ['<fsx:OutputUnits>'])
							appendToFile(7, ['<fsx:Name>' + fetchUnit(dictB034, blockette.stage_signal_output_units)[0] + '</fsx:Name>'])
							appendToFile(7, ['<fsx:Description>' + fetchUnit(dictB034, blockette.stage_signal_output_units)[1] + '</fsx:Description>'])
							appendToFile(6, ['</fsx:OutputUnits>'])
				for blockette in channel:
					if blockette.id == 54 and blockette.stage_sequence_number == 2:
						appendToFile(6, ['<fsx:OutputUnits>'])
						appendToFile(7, ['<fsx:Name>' + fetchUnit(dictB034, blockette.signal_output_units)[0] + '</fsx:Name>'])
						appendToFile(7, ['<fsx:Description>' + fetchUnit(dictB034, blockette.signal_output_units)[1] + '</fsx:Description>'])
						appendToFile(6, ['</fsx:OutputUnits>'])
				for blockette in channel:
					if blockette.id == 62:
						#value and frequency are required because the current SIS parser (v2.0) does not correctly support polynomial responses
						if not polynomialSupported:
							appendToFile(6, ['<fsx:Value>' + '0' + '</fsx:Value>'])
							appendToFile(6, ['<fsx:Frequency>' + '0' + '</fsx:Frequency>'])
						appendToFile(6, ['<fsx:InputUnits>'])
						appendToFile(7, ['<fsx:Name>' + fetchUnit(dictB034, blockette.stage_signal_in_units)[0] + '</fsx:Name>'])
						appendToFile(7, ['<fsx:Description>' + fetchUnit(dictB034, blockette.stage_signal_in_units)[1] + '</fsx:Description>'])
						appendToFile(6, ['</fsx:InputUnits>'])
						appendToFile(6, ['<fsx:OutputUnits>'])
						appendToFile(7, ['<fsx:Name>' + fetchUnit(dictB034, blockette.stage_signal_out_units)[0] + '</fsx:Name>'])
						appendToFile(7, ['<fsx:Description>' + fetchUnit(dictB034, blockette.stage_signal_out_units)[1] + '</fsx:Description>'])
						appendToFile(6, ['</fsx:OutputUnits>'])
				for blockette in channel:
					if blockette.id == 52:
						appendToFile(5, ['</fsx:InstrumentSensitivity>'])
						appendToFile(5, ['<sis:SubResponse sequenceNumber="1">'])
						appendToFile(6, ['<sis:EquipmentLink>'])
						appendToFile(7, ['<sis:SerialNumber>000</sis:SerialNumber>'])
						appendToFile(7, ['<sis:ModelName>' + fetchInstrument(dictB033, blockette.instrument_identifier) + '</sis:ModelName>'])
						appendToFile(7, ['<sis:Category>SENSOR</sis:Category>'])
						appendToFile(7, ['<sis:ComponentName>' + blockette.channel_identifier[-1] + '</sis:ComponentName>'])
						appendToFile(7, ['<sis:CalibrationDate>2199-01-23T01:23:45Z</sis:CalibrationDate>'])
						appendToFile(6, ['</sis:EquipmentLink>'])
						appendToFile(5, ['</sis:SubResponse>'])
						appendToFile(5, ['<sis:SubResponse sequenceNumber="2">'])
						appendToFile(6, ['<sis:EquipmentLink>'])
						appendToFile(7, ['<sis:SerialNumber>000</sis:SerialNumber>'])
						appendToFile(7, ['<sis:ModelName>DataLogger</sis:ModelName>'])
						appendToFile(7, ['<sis:Category>LOGGERBOARD</sis:Category>'])
						appendToFile(7, ['<sis:ComponentName>DATA1</sis:ComponentName>'])
						appendToFile(7, ['<sis:CalibrationDate>2199-01-23T01:23:45Z</sis:CalibrationDate>'])
						appendToFile(6, ['</sis:EquipmentLink>'])
						appendToFile(6, ['<sis:PreampGain>1.000000000000E+00</sis:PreampGain>'])
						appendToFile(5, ['</sis:SubResponse>'])
						appendToFile(5, ['<sis:SubResponse sequenceNumber="3">'])
						appendToFile(6, ['<sis:ResponseDictLink>'])
						appendToFile(7, ['<sis:Name>Datalogger.Filter.MS</sis:Name>'])
						appendToFile(7, ['<sis:SISNamespace>SCSN GROUP</sis:SISNamespace>'])
						appendToFile(7, ['<sis:Type>FilterSequence</sis:Type>'])
						appendToFile(6, ['</sis:ResponseDictLink>'])
						appendToFile(5, ['</sis:SubResponse>'])
				# for stage in stages(channel):
				# 	if stage > 0:
				# 		appendToFile(5, ['<fsx:Stage number="' + str(stage) + '">'])
				# 		for blockette in channel:
				# 			if blockette.id == 53 and blockette.stage_sequence_number == stage:
				# 				appendToFile(6, ['<fsx:PolesZeros>'])
				# 				appendToFile(7, ['<fsx:InputUnits>'])
				# 				appendToFile(8, ['<fsx:Name>' + fetchUnit(dictB034, blockette.stage_signal_input_units)[0] + '</fsx:Name>'])
				# 				appendToFile(8, ['<fsx:Description>' + fetchUnit(dictB034, blockette.stage_signal_input_units)[1] + '</fsx:Description>'])
				# 				appendToFile(7, ['</fsx:InputUnits>'])
				# 				appendToFile(7, ['<fsx:OutputUnits>'])
				# 				appendToFile(8, ['<fsx:Name>' + fetchUnit(dictB034, blockette.stage_signal_output_units)[0] + '</fsx:Name>'])
				# 				appendToFile(8, ['<fsx:Description>' + fetchUnit(dictB034, blockette.stage_signal_output_units)[1] + '</fsx:Description>'])
				# 				appendToFile(7, ['</fsx:OutputUnits>'])
				# 				appendToFile(7, ['<fsx:PzTransferFunctionType>' + blockettetools.describeTransferFunctionType(blockette.transfer_function_types) + '</fsx:PzTransferFunctionType>'])
				# 				appendToFile(7, ['<fsx:NormalizationFactor>' + str(blockette.A0_normalization_factor) + '</fsx:NormalizationFactor>'])
				# 				appendToFile(7, ['<fsx:NormalizationFrequency>' + str(blockette.normalization_frequency) + '</fsx:NormalizationFrequency>'])
				# 				if blockette.number_of_complex_zeros > 0:
				# 					zeros = {'real zero': [], 'imaginary zero': [], 'real zero error': [], 'imaginary zero error': []}
				# 					if blockette.number_of_complex_zeros == 1:
				# 						zeros['real zero'] = [blockette.real_zero]
				# 						zeros['imaginary zero'] = [blockette.imaginary_zero]
				# 						zeros['real zero error'] = [blockette.real_zero_error]
				# 						zeros['imaginary zero error'] = [blockette.imaginary_zero_error]
				# 					elif blockette.number_of_complex_zeros > 1:
				# 						zeros['real zero'] = blockette.real_zero
				# 						zeros['imaginary zero'] = blockette.imaginary_zero
				# 						zeros['real zero error'] = blockette.real_zero_error
				# 						zeros['imaginary zero error'] = blockette.imaginary_zero_error
				# 				for index in range(blockette.number_of_complex_zeros):
				# 					appendToFile(7, ['<fsx:Zero number="' + str(index) + '">'])
				# 					appendToFile(8, ['<fsx:Real plusError="' + str(zeros['real zero error'][index]) + '" minusError="' + str(zeros['real zero error'][index]) + '">' + str(zeros['real zero'][index]) + '</fsx:Real>'])
				# 					appendToFile(8, ['<fsx:Imaginary plusError="' + str(zeros['imaginary zero error'][index]) + '" minusError="' + str(zeros['imaginary zero error'][index]) + '">' + str(zeros['imaginary zero'][index]) + '</fsx:Imaginary>'])
				# 					appendToFile(7, ['</fsx:Zero>'])
				# 				if blockette.number_of_complex_poles > 0:
				# 					poles = {'real pole': [], 'imaginary pole': [], 'real pole error': [], 'imaginary pole error': []}
				# 					if blockette.number_of_complex_poles == 1:
				# 						poles['real pole'] = [blockette.real_pole]
				# 						poles['imaginary pole'] = [blockette.imaginary_pole]
				# 						poles['real pole error'] = [blockette.real_pole_error]
				# 						poles['imaginary pole error'] = [blockette.imaginary_pole_error]
				# 					elif blockette.number_of_complex_poles > 1:
				# 						poles['real pole'] = blockette.real_pole
				# 						poles['imaginary pole'] = blockette.imaginary_pole
				# 						poles['real pole error'] = blockette.real_pole_error
				# 						poles['imaginary pole error'] = blockette.imaginary_pole_error
				# 				for index in range(blockette.number_of_complex_poles):
				# 					appendToFile(7, ['<fsx:Pole number="' + str(index) + '">'])
				# 					appendToFile(8, ['<fsx:Real plusError="' + str(poles['real pole error'][index]) + '" minusError="' + str(poles['real pole error'][index]) + '">' + str(poles['real pole'][index]) + '</fsx:Real>'])
				# 					appendToFile(8, ['<fsx:Imaginary plusError="' + str(poles['imaginary pole error'][index]) + '" minusError="' + str(poles['imaginary pole error'][index]) + '">' + str(poles['imaginary pole'][index]) + '</fsx:Imaginary>'])
				# 					appendToFile(7, ['</fsx:Pole>'])
				# 				appendToFile(6, ['</fsx:PolesZeros>'])
				# 			if blockette.id == 54 and blockette.stage_sequence_number == stage:
				# 				appendToFile(6, ['<fsx:Coefficients>'])
				# 				appendToFile(7, ['<fsx:InputUnits>'])
				# 				appendToFile(8, ['<fsx:Name>' + fetchUnit(dictB034, blockette.signal_input_units)[0] + '</fsx:Name>'])
				# 				appendToFile(8, ['<fsx:Description>' + fetchUnit(dictB034, blockette.signal_input_units)[1] + '</fsx:Description>'])
				# 				appendToFile(7, ['</fsx:InputUnits>'])
				# 				appendToFile(7, ['<fsx:OutputUnits>'])
				# 				appendToFile(8, ['<fsx:Name>' + fetchUnit(dictB034, blockette.signal_output_units)[0] + '</fsx:Name>'])
				# 				appendToFile(8, ['<fsx:Description>' + fetchUnit(dictB034, blockette.signal_output_units)[1] + '</fsx:Description>'])
				# 				appendToFile(7, ['</fsx:OutputUnits>'])
				# 				appendToFile(7, ['<fsx:CfTransferFunctionType>' + blockettetools.describeTransferFunctionType(blockette.response_type) + '</fsx:CfTransferFunctionType>'])
				# 				appendToFile(6, ['</fsx:Coefficients>'])
				# 			if blockette.id == 57 and blockette.stage_sequence_number == stage:
				# 				appendToFile(6, ['<fsx:Decimation>'])
				# 				appendToFile(7, ['<fsx:InputSampleRate>' + str(blockette.input_sample_rate) + '</fsx:InputSampleRate>'])
				# 				appendToFile(7, ['<fsx:Factor>' + str(blockette.decimation_factor) + '</fsx:Factor>'])
				# 				appendToFile(7, ['<fsx:Offset>' + str(blockette.decimation_offset) + '</fsx:Offset>'])
				# 				appendToFile(7, ['<fsx:Delay>' + str(blockette.estimated_delay) + '</fsx:Delay>'])
				# 				appendToFile(7, ['<fsx:Correction>' + str(blockette.correction_applied) + '</fsx:Correction>'])
				# 				appendToFile(6, ['</fsx:Decimation>'])
				# 			if blockette.id == 58 and blockette.stage_sequence_number == stage:
				# 				appendToFile(6, ['<fsx:StageGain>'])
				# 				appendToFile(7, ['<fsx:Value>' + str(blockette.sensitivity_gain) + '</fsx:Value>'])
				# 				appendToFile(7, ['<fsx:Frequency>' + str(blockette.frequency) + '</fsx:Frequency>'])
				# 				appendToFile(6, ['</fsx:StageGain>'])
				# 			if blockette.id == 62 and blockette.stage_sequence_number == stage:
				# 				appendToFile(6, ['<fsx:Polynomial>'])
				# 				appendToFile(7, ['<fsx:InputUnits>'])
				# 				appendToFile(8, ['<fsx:Name>' + fetchUnit(dictB034, blockette.stage_signal_in_units)[0] + '</fsx:Name>'])
				# 				appendToFile(8, ['<fsx:Description>' + fetchUnit(dictB034, blockette.stage_signal_in_units)[1] + '</fsx:Description>'])
				# 				appendToFile(7, ['</fsx:InputUnits>'])
				# 				appendToFile(7, ['<fsx:OutputUnits>'])
				# 				appendToFile(8, ['<fsx:Name>' + fetchUnit(dictB034, blockette.stage_signal_out_units)[0] + '</fsx:Name>'])
				# 				appendToFile(8, ['<fsx:Description>' + fetchUnit(dictB034, blockette.stage_signal_out_units)[1] + '</fsx:Description>'])
				# 				appendToFile(7, ['</fsx:OutputUnits>'])
				# 				appendToFile(7, ['<fsx:ApproximationType>' + blockettetools.describeApproximationType(blockette.polynomial_approximation_type) + '</fsx:ApproximationType>'])
				# 				appendToFile(7, ['<fsx:FrequencyLowerBound>' + str(blockette.lower_valid_frequency_bound) + '</fsx:FrequencyLowerBound>'])
				# 				appendToFile(7, ['<fsx:FrequencyUpperBound>' + str(blockette.upper_valid_frequency_bound) + '</fsx:FrequencyUpperBound>'])
				# 				appendToFile(7, ['<fsx:ApproximationLowerBound>' + str(blockette.lower_bound_of_approximation) + '</fsx:ApproximationLowerBound>'])
				# 				appendToFile(7, ['<fsx:ApproximationUpperBound>' + str(blockette.upper_bound_of_approximation) + '</fsx:ApproximationUpperBound>'])
				# 				appendToFile(7, ['<fsx:MaximumError>' + str(blockette.maximum_absolute_error) + '</fsx:MaximumError>'])
				# 				if blockette.number_of_polynomial_coefficients > 0:
				# 					polyco = []
				# 					polyerror = []
				# 					if blockette.number_of_polynomial_coefficients == 1:
				# 						polyco = [blockette.polynomial_coefficient]
				# 						polyerror = [blockette.polynomial_coefficient_error]
				# 					elif blockette.number_of_polynomial_coefficients > 1:
				# 						polyco = blockette.polynomial_coefficient
				# 						polyerror = blockette.polynomial_coefficient_error
				# 					for index in range(blockette.number_of_polynomial_coefficients):
				# 						appendToFile(7, ['<fsx:Coefficient number="' + str(index) + '" plusError="' + str(polyerror[index]) + '" minusError="' + str(polyerror[index]) + '">' + str(polyco[index]) + '</fsx:Coefficient>'])
				# 				appendToFile(6, ['</fsx:Polynomial>'])
				# 				if not polynomialSupported:
				# 					#required because the current SIS parser (v2.0) does not correctly support polynomial responses
				# 					appendToFile(6, ['<fsx:StageGain>'])
				# 					appendToFile(7, ['<fsx:Value>' + '0' + '</fsx:Value>'])
				# 					appendToFile(7, ['<fsx:Frequency>' + '0' + '</fsx:Frequency>'])
				# 					appendToFile(6, ['</fsx:StageGain>'])
				# 		appendToFile(5, ['</fsx:Stage>'])
				appendToFile(4, ['</fsx:Response>'])
				appendToFile(3, ['</fsx:Channel>'])

def validDate(date):
	#this function returns a UTCDateTime date in the event a date is blank in the dataless
	if date == '':
		return UTCDateTime(2599, 12, 31, 23, 59, 59)
	else:
		return date

def noB054(channel):
	b054absent = True
	for blockette in channel:
		if blockette.id == 54:
			b054absent = False
	return b054absent

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
	elif os.path.exists('/tr1/telemetry_days/' + netsta):
		path = '/tr1/telemetry_days/' + netsta
	else:
		print 'No station ' + netsta + ' found. Please check again.'
	path = globMostRecent(globMostRecent(path))
	if os.path.exists('/dcc/metadata/dataless/DATALESS.' + netsta + '.seed'):
		#Checks to see which dataless to get abbreviation dictionaries for
		return 'rdseed -f ' + path + '/00_LHZ.512.seed -g /dcc/metadata/dataless/DATALESS.' + netsta + '.seed -a'
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
		appendToFile(4, ['<fsx:Type>' + flag.upper() + '</fsx:Type>'])

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

def channelWithB062(channel):
	for blockette in channel:
		if blockette.id == 62:
			return True
	return False

def processOutro(dataless):
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
			appendToFile(5, ['<fsx:EndEffectiveTime>' + str(validDate(blockette.end_effective_time)).split('.')[0] + '</fsx:EndEffectiveTime>'])
			appendToFile(5, ['<fsx:Author>'])
			appendToFile(6, ['<fsx:Name>' + 'USGS ASL RDSEED' + '</fsx:Name>'])
			appendToFile(5, ['</fsx:Author>'])
			appendToFile(4, ['</fsx:Comment>'])

def stages(channel):
	stages = []
	for blockette in channel:
		try:
			if blockette.stage_sequence_number not in stages:
				stages.append(blockette.stage_sequence_number)
		except:
			x = 0
	stages.sort()
	return stages

#setting global variables
parserval = getArguments()
net = parserval.net.upper()
sta = parserval.sta.upper()
outputFilename = parserval.outputFilename
if outputFilename == '*':
	#if no custom filename is given, it defaults to NN_SSSS.xml
	outputFilename = net + '_' + sta + '.fdsn.xml'
	if debug:
		print 'Your output file will be named ' + outputFilename
if '.xml' != outputFilename[-4:]:
	#appends a file extension if one isn't given
	if debug:
		print 'Output filename changed from ' + outputFilename + ' to ' + outputFilename + '.xml'
	outputFilename += '.fdsn.xml'
outputFilepath = net + '/' + outputFilename

dictB031, dictB033, dictB034 = getDictionaries(net + sta)

if isvalidnetsta.isValidNetSta(net, sta):
	processDataless(datalesstools.getStationDataless(net + sta))
else:
	print 'Network and station found to not be valid (isvalidnetsta.py)'

print 'Process lasted', int(UTCDateTime.now() - now), 'seconds'