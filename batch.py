#!/usr/bin/env python

import os
import sys

fp = open("massfiles", 'r')

files = fp.readlines()

fp.close()

for file in files:
    date = file.split('.')[0][-4:]
    year = file.split('.')[0][-8:-4]
    full = year + date
    proc_cmd = "./remass.newatmos.sh %s" % file.strip()
    sync_cmd = "/usr/bin/rsync -av %s.* nfs4::seeingdata/mass/%s/%s/." % \
        (full, year, date)
    rm_cmd = "rm %s.*" % full

    print "Processing: %s" % proc_cmd
    os.system(proc_cmd)
    print "Syncing: %s" % sync_cmd
    os.system(sync_cmd)
