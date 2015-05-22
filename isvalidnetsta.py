#!/usr/bin/env python

import sys
#
# net = sys.argv[1].upper()
# sta = sys.argv[2].upper()
# netsta = net + sta

networks = ['CU','IC','IU','IW','NE','US']

netstas  = ['CUANWB', 'CUBBGH', 'CUBCIP', 'CUGRGR', 'CUGRTK', 'CUGTBY', 'CUMTDJ',
	'CUSDDR', 'CUTGUH',
	'ICBJT', 'ICENH', 'ICHIA', 'ICKMI', 'ICLSA', 'ICMDJ', 'ICQIZ', 'ICSSE',
	'ICWMQ', 'ICXAN',
	'IUADK', 'IUAFI', 'IUANMO', 'IUANTO', 'IUBBSR', 'IUBILL', 'IUCASY',
	'IUCCM', 'IUCHTO', 'IUCOLA', 'IUCOR', 'IUCTAO', 'IUDAV', 'IUDWPF', 'IUFUNA',
	'IUFURI', 'IUGNI', 'IUGRFO', 'IUGUMO', 'IUHKT', 'IUHNR', 'IUHRV', 'IUINCN',
	'IUJOHN', 'IUKBL', 'IUKEV', 'IUKIEV', 'IUKIP', 'IUKMBO', 'IUKNTN', 'IUKONO',
	'IUKOWA', 'IULCO', 'IULSZ', 'IULVC', 'IUMA2', 'IUMACI', 'IUMAJO', 'IUMAKZ',
	'IUMBWA', 'IUMIDW', 'IUMSKU', 'IUNWAO', 'IUOTAV', 'IUPAB', 'IUPAYG', 'IUPET',
	'IUPMG', 'IUPMSA', 'IUPOHA', 'IUPTCN', 'IUPTGA', 'IUQSPA', 'IURAO', 'IURAR',
	'IURCBR', 'IURSSD', 'IUSAML', 'IUSBA', 'IUSDV', 'IUSFJD', 'IUSJG', 'IUSLBS',
	'IUSNZO', 'IUSSPA', 'IUTARA', 'IUTATO', 'IUTEIG', 'IUTIXI', 'IUTRIS',
	'IUTRQA', 'IUTSUM', 'IUTUC', 'IUULN', 'IUWAKE', 'IUWCI', 'IUWVT', 'IUXMAS',
	'IUYAK', 'IUYSS',
	'IWDLMT', 'IWFLWY', 'IWFXWY', 'IWIMW', 'IWLOHW', 'IWMFID', 'IWMOOW',
	'IWPHWY', 'IWPLID', 'IWREDW', 'IWRWWY', 'IWSMCO', 'IWSNOW', 'IWTPAW',
	'NEBCX', 'NEBRYW', 'NEEMMW', 'NEFFD', 'NEHNH', 'NEPQI', 'NEQUA2',
	'NEVT1', 'NEWES', 'NEWSPT', 'NEWVL', 'NEYLE',
	'USAAM', 'USACSO', 'USAGMN', 'USAHID', 'USAMTX', 'USBINY', 'USBLA',
	'USBMO', 'USBOZ', 'USBRAL', 'USBW06', 'USCBKS', 'USCBN', 'USCNNC', 'USCOWI',
	'USDGMT', 'USDUG', 'USECSD', 'USEGAK', 'USEGMT', 'USELK', 'USERPA', 'USEYMN',
	'USGLMI', 'USGOGA', 'USHAWA', 'USHDIL', 'USHLID', 'USHWUT', 'USISCO', 'USJCT',
	'USJFWS', 'USKSU1', 'USKVTX', 'USLAO', 'USLBNH', 'USLKWY', 'USLONY', 'USLRAL',
	'USMCWV', 'USMIAR', 'USMNTX', 'USMSO', 'USMVCO', 'USNATX', 'USNEW', 'USNHSC',
	'USNLWA', 'USOGNE', 'USOXF', 'USPKME', 'USRLMT', 'USSCIA', 'USSDCO', 'USTPNV',
	'USTZTN', 'USVBMS', 'USWMOK', 'USWRAK', 'USWUAZ', 'USWVOR']



def isValidNetSta(network, station):
	netsta = network + station
	if netsta in netstas:
		return True
	else:
		return False

# if __name__ == '__main__':
# 	print 'SUCCESS'
# 	# isValidNetSta()