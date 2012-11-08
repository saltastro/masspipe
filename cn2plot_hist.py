#!/usr/bin/env python

import sys
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
#matplotlib.use('Cairo')
#from matplotlib import rc
#rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']})
#rc('text', usetex=True)
from readREMASS import readMASS
from matplotlib.colors import LogNorm
from pylab import *
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import datetime

def format_time(x, pos=None):
    return dates.num2date(x).strftime('%H')

def cn2plot_float(massdata, outfile=None, indatetime=False, imshow=False):

    z = np.hstack(massdata['z'])
    cnsq = np.hstack(massdata['Cn2'])

    times = []
    for _ in range(int(massdata['Nz'][0])):
        times.append(massdata['time'])
        
    ut = np.hstack((np.array([massdata['time'][0]]), np.hstack(times)))
    
    if indatetime: 
       for i in range(len(ut)): 
           ut[i]=ut[i].time().hour+ut[i].time().minute/60.0+ut[i].time().second/3600.0
           if ut[i]<12: 
              ut[i]=24+ut[i]
    else:
       dut=np.zeros(len(ut), dtype=float)
       for i in range(len(ut)):
           dtut=datetime.datetime.strptime(ut[i],'%H:%M:%S')
           dut[i]=dtut.time().hour+dtut.time().minute/60.0+dtut.time().second/3600.0
           if dut[i]<12: 
              dut[i]=dut[i]+24
       ut=dut

    fig = figure()
    subplots_adjust(hspace=0.001)

    ax = fig.add_subplot(111)
    #ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
    ax.set_ylabel('Height (km)')
    ax.set_xlabel('Cn2')

    rx, ry = 1.0, 5.0
    area = rx*ry*pi
    theta = arange(0, 2*pi+0.01, 0.1)
    verts = zip(rx/area*cos(theta), ry/area*sin(theta))

    cnsq[cnsq > 5.0e-12] = 5.0e-12
    colors = cnsq
    a = cnsq*1.0e14
    c = scatter(np.log10(cnsq), z)
#    c = scatter(ut, z, c=colors, s=a, marker=None, verts=verts, norm=LogNorm(vmin=5.0e-15, vmax=5.0e-12))
#    c.set_alpha(0.25)
#    cb = colorbar()
#    cb.ax.set_ylabel('$C^2_n$', fontsize=16, rotation='horizontal')

#    xt=ax.get_xticks()
#    xl=[]
#    for i in range(len(xt)):
#        if xt[i]>=24: xt[i]=xt[i]-24
#        xl.append('%i' % xt[i])
#   ax.set_xticklabels(xl)

    ax.set_yscale('log')
    ax.set_yticks([0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0])
    ax.set_yticklabels(["0.5", "1", "2", "4", "8", "16", "32", "64"])
    ax.set_ylim([0.15,40])
    if outfile: savefig(outfile)
    if imshow: show()


if __name__=='__main__':
   indt=False
   massdata = readMASS(sys.argv[1], 'T', rtype='dict', indatetime=indt)
   outfile=None
   cn2plot_float(massdata, outfile, indatetime=indt, imshow=True)
