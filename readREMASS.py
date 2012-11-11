"""readMASS is a file that reads and parses the output to the atmos
program. The user gives it the file that they want to read, and the
line they want to return. They can also give it an option to print
out the results.  The program will return a list of arrays where each
array is an entry in the output file depending on what type of
measurement is given. There are four different types of data that
can be requested which are:

#--produce the comments from the file

A--Produce the seeing measurements from the file

T*--Produce the fixed layer CN2 measurements

W*--Produce wind profile measurements

Each of the requests will return all of the data in that file
associated with that line as a list. The individual arrays that are
returned are:

A--A,date,time,fSee,e_fSee,See,e_See,fM0,e_fM0,M0,e_M0,fHeff,
   e_fHeff,Heff,e_Heff,Isopl,e_Isopl,M2,e_M2,Tau,e_Tau
TX--T,date,time,Met,Nz,Chi2,SeeCn,z_1,Cn2_1,z_2,Cn2_2,z_3,Cn2_3,
   z_4,Cn2_4,z_5,Cn2_5,z_6,Cn2_6
TL--T,date,time,Met,Nz,Chi2,SeeCn,z_1,Cn2_1,z_2,Cn2_2,z_3,Cn2_3

Example of usage:
A,date,time,fSee,e_fSee,See,e_See,fM0,e_fM0,M0,e_M0,fHeff,e_fHeff,Heff,
e_Heff,Isopl,e_Isopl,M2,e_M2,Tau,e_Tau=readMASS('250310.atm', 'A')

The program can return either a list or dictionary by setting
rtype='list' or 'dict'

032610 SMC First version of the program
032710 SMC Added rtype and indatetime options

"""

import numpy as np
import datetime


def lineRead(olist, line, ltype):
    """Read in the comments from the file"""
    if ltype == '#':
        if line.startswith('#'):
            olist = appendlist(olist, line.strip())
    elif ltype == 'A' or ltype == 'M' or ltype == 'F':
        if line.startswith(ltype):
            olist = appendlist(olist, line)
    elif ltype.startswith('T'):
        if line.startswith(ltype[0]): 
            if line.split()[3] == ltype[1]:
                olist = appendlist(olist, line)
    elif ltype.startswith('W'):
        if line.startswith(ltype[0]): 
            if line.split()[3] == ltype[1]:
                olist = appendlist(olist, line)                
    return olist


def convert_time(ut, indatetime):
    """convert the time to decimal hours"""
    dut = np.zeros(len(ut), dtype=float)
    if indatetime:
        for i in range(len(ut)):
            dut[i] = ut[i].time().hour + \
                     ut[i].time().minute / 60.0 + \
                     ut[i].time().second / 3600.0
            if ut[i].time().hour < 12:
                dut[i] = 24 + dut[i]
    else:
        for i in range(len(ut)):
            dtut = datetime.datetime.strptime(ut[i], '%H:%M:%S')
            dut[i] = dtut.time().hour + \
                     dtut.time().minute / 60.0 + \
                     dtut.time().second / 3600.0
            if dtut.time().hour < 12:
                dut[i] = 24 + dut[i]

    return dut


def to_datetime(date, time):
    s = "%s %s" % (date, time)
    return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def fval(x):
    """If possible convert a string to float"""
    try:
        y = float(x)
    except Exception, ValueError:
        y = x
    return y


def appendlist(olist, line):
    slist = line.split()
    #first check to see if olist has been created
    if len(olist) < 1:
        for x in slist:
            olist.append([fval(x)])
    else:
        for i in range(len(slist)):
            olist[i].append(fval(slist[i]))
    return olist


def arrlist(olist, column=0):
    """For all columns appearring after column, convert to an array"""
    for i in range(column, len(olist)):
        try:
            olist[i] = np.array(olist[i])
        except:
            pass
    return olist

Mobjectlist = ['type', 'data', 'time', 'format', 'Airmass']
Fobjectlist = ['type', 'data', 'time',
               'A', 'e_A', 'B', 'e_B',
               'C', 'e_C', 'D', 'e_D']
Aobjectlist = ['type', 'date', 'time', 'fSee', 'e_fSee', 'DIMMSee',
               'e_DIMMSee', 'M0', 'e_M0', 'DIMMCn2', 'e_DIMMCn2', 'Heff',
               'e_Heff', 'Isopl', 'e_Isopl', 'M2', 'e_M2', 'Desi_Tau',
               'e_Desi_Tau', 'Tau', 'e_Tau']
Tobjectlist = ['type', 'date', 'time', 'Met', 'Nz', 'Chi2', 'SeeCn',
               'z', 'Cn2', 'e_Cn2']
Wobjectlist = ['type', 'date', 'time', 'Exp', 'Nz', 'Resid', 'Tau',
               'z', 'wind', 'e_wind']


def makedict(olist, ltype):
    """Convert list to dictonary with appropriate values"""
    odict = {}
    if ltype == 'A':
        objlist = Aobjectlist
    elif ltype == 'TX' or ltype == 'TV':
        objlist = Tobjectlist
    elif ltype == 'WV' or ltype == 'WS' or ltype == 'WL':
        objlist = Wobjectlist        
    elif ltype == 'M':
        objlist = Mobjectlist
    elif ltype == 'F':
        objlist = Fobjectlist
    else:
        return olist

    if ltype == 'TX' or ltype == 'TV':
        offset = 7
        for i in range(offset):
            odict[objlist[i]] = olist[i]
        odict['z'] = []
        odict['Cn2'] = []
        odict['e_Cn2'] = []
        for i in range(int(olist[4][0])):
            odict['z'].append(olist[offset])
            offset += 1
            odict['Cn2'].append(olist[offset])
            offset += 1
            odict['e_Cn2'].append(olist[offset])
            offset += 1
    elif ltype == 'WS' or ltype == 'WL' or ltype == 'WV':
        offset = 7
        for i in range(offset):
            odict[objlist[i]] = olist[i]
        odict['z'] = []
        odict['wind'] = []
        odict['e_wind'] = []
        for i in range(int(olist[4][0])):
            odict['z'].append(olist[offset])
            offset += 1
            odict['wind'].append(olist[offset])
            offset += 1
            odict['e_wind'].append(olist[offset])
            offset += 1
    else:
        for i in range(len(objlist)):
            odict[objlist[i]] = olist[i]

    return odict


def readMASS(massfile, ltype, rtype='list', verbose=False, indatetime=False):
    """readMASS reads in the output from the atmos program
    and returns the data in that file that is assocaited
    with that line type. Line type is the letter associated
    with that line of the file

    For different lytpes, here are the different values that
    get returned:
    '#': All the commented lines in the file
    'A': Values associated with the seeing measurement
    'T': Values associated with Cn2(h) calculation.
    'M': Values associated with corrected flux measured by the MASS

    The program can return either a list or dictionary by setting
    rtype='list' or 'dict'

    In datetime returns the time as a datetime object
    """
    olist = []

    #open the file
    try:
        fin = open(massfile)
        lines = fin.readlines()
        fin.close()
    except Exception, IOErrer:
        print 'Could not open file %s' % massfile
        return olist

    #set the function that will read in the values
    if ltype not in ['#', 'A', 'TV', 'TX', 'WS', 'WL', 'WV', 'F', 'M']:
        print 'ltype %s is not an accepted format' % ltype
        return olist

    #enter in the values
    for l in lines:
        olist = lineRead(olist, l, ltype)

    #set up the time as a date time object
    if indatetime and ltype != '#':
        for i in range(len(olist[2])):
            olist[2][i] = to_datetime(olist[1][i], olist[2][i])

    #for certain types, normalize the lists to arrays
    if ltype != '#':
        olist = arrlist(olist, 0)

    #convert to dictionary if requested
    if rtype == 'dict':
        olist = makedict(olist, ltype)

    #print out the results if requested
    if verbose:
        if rtype == 'list':
            for i in olist:
                print i
        if rtype == 'dict':
            for i in olist:
                print i, olist[i]

    #return the list of values
    return olist

if __name__ == '__main__':
    import sys
    infile = sys.argv[1]
    ltype = sys.argv[2]
    print 'Testing list'
    #readMASS(infile, ltype, rtype='list', verbose=True)
    print 'Testing dict'
    readMASS(infile, ltype, rtype='dict', verbose=True, indatetime=True)
