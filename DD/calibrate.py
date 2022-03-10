import os
import sys

'''
    This code does the calibration via runwscleanauto.
    It needs the region file in the folder, along with the splitted measurement set.
    It runs after standalone_peel, but it requires a copy step where the splitted MS + boxfile
    are copied to a dedicated folder.
    Output: a lot of files, images, losoto-plots and merged.h5
'''

ROOT_FOLDER = '/net/rijn/data2/groeneveld/LoDeSS_files/'
HELPER_SCRIPTS = '/net/rijn/data2/rvweeren/LoTSS_ClusterCAL/'
FACET_PIPELINE = ROOT_FOLDER + 'lofar_facet_selfcal/facetselfcal.py'
H5_HELPER = '/net/rijn/data2/groeneveld/lofar_helpers/'

CHOUT = 12
STOP  =  6

peelnum = sys.argv[1]
callstring = f"python {FACET_PIPELINE} --helperscriptspath={HELPER_SCRIPTS} --helperscriptspathh5merge={H5_HELPER} -b Dir{peelnum}.reg --skipbackup --startfromtgss --usemodeldataforsolints --usewgridder True --channelsout={CHOUT} --stop={STOP} --uvmin=60 --docircular --BLsmooth Dir{peelnum}.*.peel.ms"
os.system(callstring)
