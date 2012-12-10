"""
readDIMM reads in and parses the output from robodimm file.
It will return either a list or dictionary with an entry
for each column in the file.   It can read in either the seeing.log
file or the seeing1t2.log file

Example of usage:


The program can return either a list or dictionary by setting
rtype='list' or 'dict'

032610  SMC   First version of the program
032710  SMC   Added rtype and indatetime options

"""

import numpy
import datetime


#massdimmseeinglist=['date','time','HR','name','z','n_image',
#'FWHN_transverse','FWHM','FWHM_longitude','r0','flux', 'dx', 'dy']
massdimmseeinglist = ['date', 'time', 'var_s', 'var_l', 'seeing',
                      'seeing_l', 'seeing_corr', 'airmass']
massdimmt1t2list = ['HR', 'date', 'time', 'n_t1', 'FWHM_t1',
                    'FWHM_transverse_t1', 'FWHM_longitude_t1', 'flux_t1',
                    'noise_t1', 'scint1_t1', 'scint2_t1', 'strehl1_t1',
                    'strehl2_t1', 'n_t2', 'FWHM_t2', 'FWHM_transverse_t2',
                    'FWHM_longitude_t2', 'flux_t2', 'noise_t2', 'scint1_t2',
                    'scint2_t2', 'strehl1_t2', 'strehl2_t2',
                    'extra1', 'extra2']


def lineRead(olist, line):
    """
    Read in the lines from the file and append them into the list
    """
    if line != '#':
        olist = appendlist(olist, line)
    return olist


def converttime(date, time):
    s = "%s %s" % (date, time)
    return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def fval(x):
    """
    If possible convert a string to float
    """
    try:
        y = float(x)
    except:
        y = x
    return y


def appendlist(olist, line):
    slist = line.split()
    #first check to see if olist has been created
    if not olist:
        for x in slist:
            olist.append([fval(x)])
    else:
        for i in range(len(slist)):
            olist[i].append(fval(slist[i]))
    return olist


def arrlist(olist, column=0):
    """
    For all columns appearring after column, convert to an array
    """
    for i in range(column, len(olist)):
        try:
            olist[i] = numpy.array(olist[i])
        except:
            pass
    return olist


def makedict(olist, ftype):
    """
    Convert list to dictonary with appropriate values
    """
    odict = {}
    if ftype == 'seeing':
        objlist = massdimmseeinglist
    elif ftype == 't1t2':
        objlist = massdimmt1t2list
    else:
        return olist
    for i in range(len(objlist)):
        odict[objlist[i]] = olist[i]
    return odict


def readDIMM(dimmfile, ftype='seeing', rtype='list', verbose=False,
             indatetime=False):
    """
    readDIMM reads in the output from the robodimm program
    and returns the data in that file depending on what type of file
    it is. ftype is the type of file eitehr 'seeing' or 't1t2'.
    'seeing' is the default.

    The returned values depend on the options:
    'seeing'-- 'date','time','HR','name','z','n_image',
               'FWHN_transverse','FWHM','FWHM_longitude','r0',
               'flux', 'dx', 'dy'
    't1t2' -- 'HR', 'date','time', 'n_t1', 'FWHM_t1', 'FWHM_transverse_t1',
              'FWHM_longitude_t1', 'flux_t1', 'noise_t1', 'scint1_t1',
              'scint2_t1', 'strehl1_t1', 'strehl2_t1',
              'n_t2', 'FWHM_t2', 'FWHM_transverse_t2',
              'FWHM_longitude_t2', 'flux_t2', 'noise_t2',
              'scint1_t2', 'scint2_t2', 'strehl1_t2', 'strehl2_t2',
              'extra1', 'extra2'

    't1t2'--

    The program can return either a list or dictionary by setting
    rtype='list' or 'dict'

    In datetime returns the time as a datetime object
    """

    #set up any variables
    olist = []

    #open the file
    try:
        fin = open(dimmfile)
    except:
        print 'Could not open file %s' % dimmfile
        return olist

    #set the function that will read in the values
    if ftype not in ['seeing', 't1t2']:
        print 'fytpe %s is not an accepted format' % ftype
        return olist

    #enter in the values
    for f in fin:
        try:
            olist = lineRead(olist, f)
        except Exception, e:
            print e

    #close the file
    fin.close()
    #fix the name
    #if ftype=='seeing':
    #   for i in range(len(olist[3])):
    #       olist[3][i] += ' '+olist[4][i]
    #   olist.remove(olist[4])
    #set up the time as a date time object
    if indatetime:
        tcol = 1
        if ftype == 't1t2':
            tcol = 2
        for i in range(len(olist[tcol])):
            olist[tcol][i] = converttime(olist[tcol - 1][i], olist[tcol][i])

    #for certain types, normalize the lists to arrays
    olist = arrlist(olist, 0)

    #convert to dictionary if requested
    if rtype == 'dict':
        olist = makedict(olist, ftype)

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
    ftype = sys.argv[2]
    print 'Testing list'
    #readDIMM(infile, ftype, rtype='list', verbose=True)
    print 'Testing dict'
    readDIMM(infile, ftype, rtype='dict', verbose=False, indatetime=True)
