#!/usr/bin/env python

from obspy.core import UTCDateTime

blkt = {}

def 50():
	blkt['description'] = 'Station Identifier Blockette'
	blkt['blockette type'] = 0
	blkt['length of blockette'] = 0
	blkt['station_call_letters'] = ''
	blkt['latitude'] = 0.0
	blkt['longitude'] = 0.0
	blkt['elevation'] = 0.0
	blkt['number of channels'] = 0
	blkt['number of station comments'] = 0
	blkt['site name'] = ''
	blkt['network identifier code'] = 0
	blkt['32 bit word order'] = 0
	blkt['16 bit word order'] = 0
	blkt['start effective date'] = UTCDateTime(1985, 1, 16, 0, 0)
	blkt['end effective date'] = UTCDateTime(2599, 12, 31, 23, 59, 59)
	blkt['update flag'] = ''
	blkt['network code'] = ''
	return blkt

def 52():
	blkt['description'] = 'Channel Identifier Blockette'
	blkt['blockette type'] = 0
	blkt['length of blockette'] = 0
	blkt['location identifier'] = ''
	blkt['channel identifier'] = ''
	blkt['subchannel identifier'] = 0
	blkt['instrument identifier'] = 0
	blkt['optional comment'] = ''
	blkt['units of signal response'] = 0
	blkt['units of calibration input'] = 0
	blkt['latitude'] = 0.0
	blkt['longitude'] = 0.0
	blkt['elevation'] = 0.0
	blkt['local depth'] = 0.0
	blkt['azimuth'] = 0.0
	blkt['dip'] = 0.0
	blkt['data format identifier code'] = 0
	blkt['data record length'] = 0
	blkt['sample rate'] = 0.0
	blkt['max clock drift'] = 0.0
	blkt['number of comments'] = 0
	blkt['channel flags'] = ''
	blkt['start date'] = UTCDateTime(1985, 1, 16, 0, 0)
	blkt['end date'] = UTCDateTime(2599, 12, 31, 23, 59, 59)
	blkt['update flag'] = ''
	return blkt

def 53():
	blkt['description'] = 'Response (Poles & Zeros) Blockette'
	blkt['blockette type'] = 0
	blkt['length of blockette'] = 0
	blkt['transfer function types'] = ''
	blkt['stage sequence number'] = 0
	blkt['stage signal input units'] = 0
	blkt['stage signal output units'] = 0
	blkt['AO normalization factor'] = 0.0
	blkt['normalization frequency'] = 0.0
	blkt['number of complex zeros'] = 0
	blkt['real zero'] = []
	blkt['imaginary zero'] = []
	blkt['real zero error'] = []
	blkt['imaginary zero error'] = []
	blkt['number of comlex poles'] = 0
	blkt['real pole'] = []
	blkt['imaginary pole'] = []
	blkt['real pole error'] = []
	blkt['imaginary pole error'] = []
	return blkt

def 54():
	blkt['description'] = ''
	blkt['blockette type'] = 0
	blkt['length of blockette'] = 0
	blkt['response type'] = ''
	blkt['stage sequence number'] = 0
	blkt['signal input units'] = 0
	blkt['signal output units'] = 0
	blkt['number of numerators'] = 0
	blkt['numerator coefficient'] = 0.0
	blkt['numerator error'] = 0.0
	blkt['number of denominators'] = 0
	blkt['denominator coefficient'] = 0.0
	blkt['denominator error'] = 0.0
	return blkt

def 57():
	blkt['description'] = ''
	blkt['blockette type'] = 0
	blkt['length of blockette'] = 0
	blkt['stage sequence number'] = 0
	blkt['input sample rate'] = 0.0
	blkt['decimation factor'] = 0
	blkt['decimation offset'] = 0
	blkt['estimated delay'] = 0.0
	blkt['correction applied'] = 0.0
	return blkt

def 58():
	blkt['description'] = ''
	blkt['blockette type'] = 0
	blkt['length of blockette'] = 0
	blkt['stage sequence number'] = 0
	blkt['sensitivity gain'] = 0.0
	blkt['frequency'] = 0.0
	blkt['number of history values'] = 0
	return blkt

def 59():
	blkt['description'] = ''
	blkt['blockette type'] = 0
	blkt['length of blockette'] = 0
	blkt['beginning effective time'] = UTCDateTime(1985, 1, 16, 0, 0)
	blkt['end effective time'] = UTCDateTime(2599, 12, 31, 23, 59, 59)
	blkt['comment code key'] = 0
	blkt['comment level'] = 0
	return blkt

def 62():
	blkt['description'] = ''
	blkt['blockette type'] = 0
	blkt['length of blockette'] = 0
	blkt[''] = ''
	blkt[''] = ''
	blkt[''] = ''
	blkt[''] = ''
	blkt[''] = ''
	blkt[''] = ''
	blkt[''] = ''
	blkt[''] = ''
	blkt[''] = ''
	blkt[''] = ''
	blkt[''] = ''
	blkt[''] = ''
	blkt[''] = ''
	blkt[''] = ''
	blkt[''] = ''
	blkt[''] = ''
	blkt[''] = ''
	blkt[''] = ''
	blkt[''] = ''
	return blkt
	
# AT THE END CHECK FOR CORRECT SPELLING