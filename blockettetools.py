#!/usr/bin/env python

from obspy.core import UTCDateTime

def skeleton50():
	blkt = {}
	blkt['description'] = 'Station Identifier Blockette'
	blkt['blockette type'] = 0
	blkt['length of blockette'] = 0
	blkt['station call letters'] = ''
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

def skeleton51(blockette):
	blkt = {}
	blkt['description'] = 'Station Comment Blockette'
	blkt['blockette type'] = 0
	blkt['length of blockette'] = 0
	blkt['beginning effective time'] = UTCDateTime(1985, 1, 16, 0, 0)
	blkt['end effective time'] = UTCDateTime(2599, 12, 31, 23, 59, 59)
	blkt['comment code key'] = 0
	blkt['comment level'] = 0
	return blkt

def skeleton52():
	blkt = {}
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

def skeleton53():
	blkt = {}
	blkt['description'] = 'Response (Poles & Zeros) Blockette'
	blkt['blockette type'] = 0
	blkt['length of blockette'] = 0
	blkt['transfer function type'] = ''
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

def skeleton54():
	blkt = {}
	blkt['description'] = 'Response (Coefficients) Blockette'
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

def skeleton57():
	blkt = {}
	blkt['description'] = 'Decimation Blockette'
	blkt['blockette type'] = 0
	blkt['length of blockette'] = 0
	blkt['stage sequence number'] = 0
	blkt['input sample rate'] = 0.0
	blkt['decimation factor'] = 0
	blkt['decimation offset'] = 0
	blkt['estimated delay'] = 0.0
	blkt['correction applied'] = 0.0
	return blkt

def skeleton58():
	blkt = {}
	blkt['description'] = 'Channel Sensitivity/Gain Blockette'
	blkt['blockette type'] = 0
	blkt['length of blockette'] = 0
	blkt['stage sequence number'] = 0
	blkt['sensitivity/gain'] = 0.0
	blkt['frequency'] = 0.0
	blkt['number of history values'] = 0
	return blkt

def skeleton59():
	blkt = {}
	blkt['description'] = 'Channel Comment Blockette'
	blkt['blockette type'] = 0
	blkt['length of blockette'] = 0
	blkt['beginning effective time'] = UTCDateTime(1985, 1, 16, 0, 0)
	blkt['end effective time'] = UTCDateTime(2599, 12, 31, 23, 59, 59)
	blkt['comment code key'] = 0
	blkt['comment level'] = 0
	return blkt

def skeleton62():
	blkt = {}
	blkt['description'] = 'Response Polynomial Blockette'
	blkt['blockette type'] = 0
	blkt['length of blockette'] = 0
	blkt['transfer function type'] = ''
	blkt['stage sequence number'] = 0
	blkt['stage signal in units'] = 0
	blkt['stage signal out units'] = 0
	blkt['polynomial approximation type'] = ''
	blkt['valid frequency units'] = ''
	blkt['lower valid frequency bound'] = 0.0
	blkt['upper valid frequency bound'] = 0.0
	blkt['maximum absolute error'] = 0.0
	blkt['number of polynomial coeffecients'] = 0
	blkt['polynomial coefficient'] = []
	blkt['polynomial coefficient error'] = []
	return blkt

def parseBlockette(blockette):
	blkt = {}
	if   blockette.id == 50:
		return blockette50(blockette)
	elif blockette.id == 51:
		return blockette51(blockette)
	elif blockette.id == 52:
		return blockette52(blockette)
	elif blockette.id == 53:
		return blockette53(blockette)
	elif blockette.id == 54:
		return blockette54(blockette)
	elif blockette.id == 57:
		return blockette57(blockette)
	elif blockette.id == 58:
		return blockette58(blockette)
	elif blockette.id == 59:
		return blockette59(blockette)
	elif blockette.id == 62:
		return blockette62(blockette)
	else:
		print 'Invalid blockette or blockette not supported'

def blockette50(blockette):
	blkt = {}
	blkt['description'] = 'Station Identifier Blockette'
	blkt['blockette type'] = blockette.blockette_type
	blkt['length of blockette'] = blockette.length_of_blockette
	blkt['station call letters'] = blockette.station_call_letters
	blkt['latitude'] = blockette.latitude
	blkt['longitude'] = blockette.longitude
	blkt['elevation'] = blockette.elevation
	blkt['number of channels'] = blockette.number_of_channels
	blkt['number of station comments'] = blockette.number_of_station_comments
	blkt['site name'] = blockette.site_name
	blkt['network identifier code'] = blockette.network_identifier_code
	blkt['32 bit word order'] = blockette.word_order_32bit
	blkt['16 bit word order'] = blockette.word_order_16bit
	blkt['start effective date'] = blockette.start_effective_date
	blkt['end effective date'] = blockette.end_effective_date
	blkt['update flag'] = blockette.update_flag
	blkt['network code'] = blockette.network_code
	return blkt

def blockette51(blockette):
	blkt = {}
	blkt['description'] = 'Station Comment Blockette'
	blkt['blockette type'] = blockette.blockette_type
	blkt['length of blockette'] = blockette.length_of_blockette
	blkt['beginning effective time'] = blockette.beginning_effective_time
	blkt['end effective time'] = blockette.end_effective_time
	blkt['comment code key'] = blockette.comment_code_key
	blkt['comment level'] = blockette.comment_level
	return blkt

def blockette52(blockette):
	blkt = {}
	blkt['description'] = 'Channel Identifier Blockette'
	blkt['blockette type'] = blockette.blockette_type
	blkt['blockette type'] = blockette.length_of_blockette
	blkt['location identifier'] = blockette.location_identifier
	blkt['channel identifier'] = blockette.channel_identifier
	blkt['subchannel identifier'] = blockette.subchannel_identifier
	blkt['instrument identifier'] = blockette.instrument_identifier
	blkt['optional comment'] = blockette.optional_comment
	blkt['units of signal response'] = blockette.units_of_signal_response
	blkt['units of calibration input'] = blockette.units_of_calibration_input
	blkt['latitude'] = blockette.latitude
	blkt['longitude'] = blockette.longitude
	blkt['elevation'] = blockette.elevation
	blkt['local depth'] = blockette.local_depth
	blkt['azimuth'] = blockette.azimuth
	blkt['dip'] = blockette.dip
	blkt['data format identifier code'] = blockette.data_format_identifier_code
	blkt['data record length'] = blockette.data_record_length
	blkt['sample rate'] = blockette.sample_rate
	blkt['max clock drift'] = blockette.max_clock_drift
	blkt['number of comments'] = blockette.number_of_comments
	blkt['channel flags'] = blockette.channel_flags
	blkt['start date'] = blockette.start_date
	blkt['end date'] = blockette.end_date
	blkt['update flag'] = blockette.update_flag
	return blkt

def blockette53(blockette):
	blkt = {}
	blkt['description'] = 'Response (Poles & Zeros) Blockette'
	blkt['blockette type'] = blockette.blockette_type
	blkt['blockette type'] = blockette.length_of_blockette
	blkt['transfer function type'] = blockette.transfer_function_types
	blkt['stage sequence number'] = blockette.stage_sequence_number
	blkt['stage signal input units'] = blockette.stage_signal_input_units
	blkt['stage signal output units'] = blockette.stage_signal_output_units
	blkt['AO normalization factor'] = blockette.A0_normalization_factor
	blkt['normalization frequency'] = blockette.normalization_frequency
	blkt['number of complex zeros'] = blockette.number_of_complex_zeros
	if blkt['number of complex zeros'] > 0:
		blkt['real zero'] = blockette.real_zero
		blkt['imaginary zero'] = blockette.imaginary_zero
		blkt['real zero error'] = blockette.real_zero_error
		blkt['imaginary zero error'] = blockette.imaginary_zero_error
	blkt['number of comlex poles'] = blockette.number_of_complex_poles
	if blkt['number of comlex poles'] > 0:
		blkt['real pole'] = blockette.real_pole
		blkt['imaginary pole'] = blockette.imaginary_pole
		blkt['real pole error'] = blockette.real_pole_error
		blkt['imaginary pole error'] = blockette.imaginary_pole_error
	return blkt

def blockette54(blockette):
	blkt = {}
	blkt['description'] = 'Response (Coefficients) Blockette'
	blkt['blockette type'] = blockette.blockette_type
	blkt['blockette type'] = blockette.length_of_blockette
	blkt['response type'] = blockette.response_type
	blkt['stage sequence number'] = blockette.stage_sequence_number
	blkt['signal input units'] = blockette.signal_input_units
	blkt['signal output units'] = blockette.signal_output_units
	blkt['number of numerators'] = blockette.number_of_numerators
	if blkt['stage sequence number'] == 3 and blkt['number of numerators'] > 0:
		blkt['numerator coefficient'] = blockette.numerator_coefficient
		blkt['numerator error'] = blockette.numerator_error
	blkt['number of denominators'] = blockette.number_of_denominators
	if blkt['stage sequence number'] == 3 and blkt['number of denominators'] > 0:
		blkt['denominator coefficient'] = blockette.denominator_coefficient
		blkt['denominator error'] = blockette.denominator_error
	return blkt

def blockette57(blockette):
	blkt = {}
	blkt['description'] = 'Decimation Blockette'
	blkt['blockette type'] = blockette.blockette_type
	blkt['blockette type'] = blockette.length_of_blockette
	blkt['stage sequence number'] = blockette.stage_sequence_number
	blkt['input sample rate'] = blockette.input_sample_rate
	blkt['decimation factor'] = blockette.decimation_factor
	blkt['decimation offset'] = blockette.decimation_offset
	blkt['estimated delay'] = blockette.estimated_delay
	blkt['correction applied'] = blockette.correction_applied
	return blkt

def blockette58(blockette):
	blkt = {}
	blkt['description'] = 'Channel Sensitivity/Gain Blockette'
	blkt['blockette type'] = blockette.blockette_type
	blkt['blockette type'] = blockette.length_of_blockette
	blkt['stage sequence number'] = blockette.stage_sequence_number
	blkt['sensitivity/gain'] = blockette.sensitivity_gain
	blkt['frequency'] = blockette.frequency
	blkt['number of history values'] = blockette.number_of_history_values
	return blkt

def blockette59(blockette):
	blkt = {}
	blkt['description'] = 'Channel Comment Blockette'
	blkt['blockette type'] = blockette.blockette_type
	blkt['length of blockette'] = blockette.length_of_blockette
	blkt['beginning effective time'] = blockette.beginning_of_effective_time
	blkt['end effective time'] = blockette.end_effective_time
	blkt['comment code key'] = blockette.comment_code_key
	blkt['comment level'] = blockette.comment_level
	return blkt

def blockette62(blockette):
	blkt = {}
	blkt['description'] = 'Response Polynomial Blockette'
	blkt['blockette type'] = blockette.blockette_type
	blkt['blockette type'] = blockette.length_of_blockette
	blkt['transfer function type'] = blockette.transfer_function_type
	blkt['stage sequence number'] = blockette.stage_sequence_number
	blkt['stage signal in units'] = blockette.stage_signal_in_units
	blkt['stage signal out units'] = blockette.stage_signal_out_units
	blkt['polynomial approximation type'] = blockette.polynomial_approximation_type
	blkt['valid frequency units'] = blockette.valid_frequency_units
	blkt['lower valid frequency bound'] = blockette.lower_valid_frequency_bound
	blkt['upper valid frequency bound'] = blockette.upper_valid_frequency_bound
	blkt['maximum absolute error'] = blockette.maximum_absolute_error
	blkt['number of polynomial coeffecients'] = blockette.number_of_polynomial_coefficients
	blkt['polynomial coefficient'] = blockette.polynomial_coefficient
	blkt['polynomial coefficient error'] = blockette.polynomial_coefficient_error
	return blkt

def describeChannelFlags(flags):
	#for describing the channel flags of blockette 52
	channelFlag = []
	dictionary = {'T': 'Triggered', 'C': 'Continuous', 'H': 'State of Health', 'G': 'Geophysical', 'W': 'Weather (or Environmental Data)', 'F': 'Flag Information', 'S': 'Synthesized Data', 'I': 'Calibration Input', 'E': 'Experimental (or Temporary)', 'M': 'Maintenance Tests', 'B': 'Beam Synthesis'}
	for flag in flags:
		channelFlag.append(dictionary[flag])
	return channelFlag

def describeTransferFunctionType(value):
	#for describing the transfer function type of blockette 53
	if value == 'A':
		return 'Laplace (radians/second)'.upper()
	elif value == 'B':
		return 'Analog (Hertz)'.upper()
	elif value == 'C':
		return 'Composite'.upper()
	elif value == 'D':
		return 'Digital (Z-Transform)'.upper()
	else:
		return 'Undefined'.upper()

def describeResponseType(value):
	#for describing the response type of blockette 54
	if value == 'A':
		return 'Laplace (radians/second)'.upper()
	elif value == 'B':
		return 'Analog (Hertz)'.upper()
	elif value == 'C':
		return 'Composite'.upper()
	elif value == 'D':
		return 'Digital'.upper()	#(Z-Transform)
	else:
		return 'Undefined'.upper()

def getChannel(loc, chan, time, dataless):
	channel = []
	endDate = UTCDateTime(2599, 12,31, 23, 59, 59)
	specifiedChannel = False
	for blockette in dataless:
		if blockette.id == 52:
			if blockette.end_date != '':
				endDate == blockette.end_date
			if blockette.location_identifier == loc and blockette.channel_identifier == chan and blockette.start_date <= time <= endDate:
				specifiedChannel = True
			else:
				specifiedChannel = False
		if specifiedChannel:
			channel.append(blockette)
	return channel

def getChannels(dataless, time):
	channels = []
	endDate = UTCDateTime(2599, 12,31, 23, 59, 59)
	isOpenChannelEpoch = False
	for blockette in dataless:
		if blockette.id == 52:
			if blockette.end_date != '':
				endDate == blockette.end_date
			if isOpenChannelEpoch:
				channels.append(channel)
			if blockette.start_date <= time <= endDate:
				isOpenChannelEpoch = True
				channel = []
			else:
				isOpenChannelEpoch = False
		if isOpenChannelEpoch:
			channel.append(blockette)
	return channels