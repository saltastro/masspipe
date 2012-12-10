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


def cn2plot_image(massdata,
                  cn2data,
                  dimmfile=None,
                  outfile=None,
                  indatetime=False,
                  imageshow=False):

    if dimmfile:
        dimmdict = readDIMM(dimmfile, ftype='seeing', rtype='dict')
        dimm_ut = convert_time(dimmdict['time'], indatetime)

    z = cn2data['z']
    cnsq = cn2data['Cn2']
    fseeing = massdata['fSee']
    e_fseeing = massdata['e_fSee']
    mut = massdata['time']
    ut = cn2data['time']
    nlayers = len(z)

    mut = convert_time(mut, indatetime)
    ut = convert_time(ut, indatetime)

    minutes = 60 * ut
    first = int(minutes[0])
    last = int(minutes[-1]) + 1
    nmin = last - first

    turb_im = np.zeros((int(nmin / 2) + 1, nlayers))
    cnsq_t = transpose(cnsq)

    for i in range(0, len(minutes)):
        index = int(0.5 * (minutes[i] - first))
        turb_im[index] = cnsq_t[i]

    turb = transpose(turb_im)
    f, (ax1, ax2) = subplots(2, sharex=True)
    f.subplots_adjust(hspace=0.1)
    f.subplots_adjust(bottom=0.1,
                      right=0.8,
                      top=0.9)
    ax2.set_ylabel('Height (km)')
    ax1.set_ylabel('Seeing (arcsec)')
    #ax1.set_aspect(2.0, adjustable='box-forced', anchor='SW')
    ax2.set_xlabel('UT')

    seeing = turb / 6.95e-13
    seeing[seeing < 0.01] = 0.01
    implot = ax2.imshow(seeing,
                        norm=LogNorm(vmin=0.01, vmax=2.0),
                        cmap=cm.get_cmap("hot_r"),
                        aspect='auto',
                        origin='lower',
                        interpolation='gaussian',
                        extent=(ut[0], ut[-1], 0, nlayers))
    cax = axes([0.85, 0.1, 0.025, 0.3825])
    cb = f.colorbar(implot, cax=cax)
    cb.ax.set_ylabel('Seeing FWHM', fontsize=12, rotation=270)
    cb.set_ticks([0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0])
    cb.ax.set_yticklabels(["0.01\"", "0.05\"", "0.1\"", "0.25\"",
                           "0.5\"", "1.0\"", "2.0\""])
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
    for i in range(int(cn2data['Nz'][0])):
        labels.append("%s" % cn2data['z'][i][0])
    ax2.set_yticklabels(labels)

    ax1.set_ylim([0, 4])
    ax1.errorbar(mut, fseeing, yerr=e_fseeing, fmt=None, label='MASS')
    if dimmfile:
        ax1.scatter(dimm_ut,
                    dimmdict['seeing'],
                    alpha=0.3,
                    label='DIMM',
                    color='red')
        ax1.legend(loc=0)

    if outfile:
        f.set_figheight(9)
        f.set_figwidth(6.5)
        savefig(outfile)
    if imageshow:
        show(block=True)

if __name__ == '__main__':
    indt = True
    cn2data = readMASS(sys.argv[1], 'TX', rtype='dict', indatetime=indt)
    massdata = readMASS(sys.argv[1], 'A', rtype='dict', indatetime=indt)
    outfile = None
    dimmfile = None

    if len(sys.argv) == 3:
        outfile = sys.argv[2]

    if len(sys.argv) == 4:
        outfile = sys.argv[3]
        dimmfile = sys.argv[2]

    cn2plot_image(massdata,
                  cn2data,
                  dimmfile,
                  outfile,
                  indatetime=indt,
                  imageshow=True)
