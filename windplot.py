#!/usr/bin/env python

import sys
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
#matplotlib.use('Cairo')
#from matplotlib import rc
#rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']})
#rc('text', usetex=True)
from readREMASS import readMASS, convert_time
from readDIMM import readDIMM
from matplotlib.colors import LogNorm
from pylab import *
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import datetime


def windplot(winddata,
             outfile=None,
             indatetime=False,
             imageshow=False):

    z = winddata['z']
    wind = winddata['wind']
    tau = winddata['Tau']
    ut = winddata['time']
    nlayers = len(z)

    ut = convert_time(ut, indatetime)

    minutes = 60 * ut
    first = int(minutes[0])
    last = int(minutes[-1]) + 1
    nmin = last - first

    wind_im = np.zeros((nmin, nlayers))
    wind_t = transpose(wind)

    for i in range(len(minutes)):
        index = int(minutes[i] - first)
        wind_im[index] = wind_t[i]

    wind = transpose(wind_im)
    f, (ax1, ax2) = subplots(2, sharex=True)
    f.subplots_adjust(hspace=0.1)
    f.subplots_adjust(bottom=0.1,
                      right=0.8,
                      top=0.9)
    ax2.set_ylabel('Height (km)')
    ax1.set_ylabel('Tau (ms)')
    #ax1.set_aspect(2.0, adjustable='box-forced', anchor='SW')
    ax2.set_xlabel('UT')

    wind[wind < 0.01] = 0.01
    implot = ax2.imshow(wind,
                        norm=LogNorm(vmin=0.01, vmax=50.0),
                        cmap=cm.get_cmap("hot_r"),
                        aspect='auto',
                        origin='lower',
                        interpolation='bicubic',
                        extent=(ut[0], ut[-1], 0, nlayers))
    cax = axes([0.85, 0.1, 0.025, 0.3825])
    cb = f.colorbar(implot, cax=cax)
    cb.ax.set_ylabel('Wind Speed (m/s)', fontsize=12, rotation=270)
#    cb.set_ticks([0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0])
#    cb.ax.set_yticklabels(["0.01\"", "0.05\"", "0.1\"", "0.25\"", \
#                           "0.5\"", "1.0\"", "2.0\""])
    xt = ax1.get_xticks()
    xl = []
    for i in range(len(xt)):
        if xt[i] >= 24:
            xt[i] = xt[i] - 24
        xl.append('%i' % xt[i])
    ax1.set_xticklabels(xl)
    ax1.set_xlim(ut[0], ut[-1])
    ax1.grid(True)
    ax2.grid(True)
    ax2.set_yticks(0.5 + np.arange(nlayers))
    labels = []
    for i in range(int(winddata['Nz'][0])):
        labels.append("%s" % winddata['z'][i][0])
    ax2.set_yticklabels(labels)

    ax1.set_ylim([0, 15])
    ax1.scatter(ut, tau)

    if outfile:
        f.set_figheight(9)
        f.set_figwidth(6.5)
        savefig(outfile)
    if imageshow:
        show(block=True)

if __name__ == '__main__':
    indt = True
    winddata = readMASS(sys.argv[1], 'WL', rtype='dict', indatetime=indt)
    outfile = None
    dimmfile = None

    if len(sys.argv) == 3:
        outfile = sys.argv[2]

    windplot(winddata,
             outfile,
             indatetime=indt,
             imageshow=True)
