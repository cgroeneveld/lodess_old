import numpy as np
import tables as tab
import argparse

def getAntAxis(soltab):
    ants = soltab.ant
    axes = str(weights.attrs['AXES']).split(',')
    return axes.index('ant')

def buildSlice(weight,antaxis,index):
    inds = [slice(None)]*weight.ndim
    inds[antaxis] = index
    return inds

parser = argparse.ArgumentParser()
parser.add_argument('tocopy',type=str)
parser.add_argument('to_apply',type=str)
parser.add_argument('-s','--soltab',type=str,default='phase000',help='look in this soltab for flags')

args = vars(parser.parse_args())

soltab = getattr(tab.open_file(args['tocopy']).root.sol000,args['soltab'])
weights = soltab.weight
ants = soltab.ant
antindex = getAntAxis(soltab)

flagged_ants = []

for i in range(weights.shape[antindex]):
    antname = str(ants[i])
    arr = np.array(weights)[buildSlice(weights,antindex,i)]
    if np.mean(arr) < 0.05:
        print(f"Flagging antenna: {antname}   -   {(1-np.mean(arr))*100}% flagged")
        flagged_ants.append(i)

writefile = tab.open_file(args['to_apply'],mode='r+')
solset = writefile.root.sol000
phases = solset.phase000
amps = solset.amplitude000

antindex_towrite = getAntAxis(amps)
phaseweights = np.array(phases.weight)
ampweights = np.array(amps.weight)
for ii in range(phases.weight.shape[antindex_towrite]):
    if ii in flagged_ants:
        antslice = buildSlice(phases.weight,antindex_towrite,ii) 
        phaseweights[antslice] = np.zeros_like(phaseweights[antslice])
        ampweights[antslice] = np.zeros_like(ampweights[antslice])

writefile.root.sol000.phase000.weight[:] = phaseweights
writefile.root.sol000.amplitude000.weight[:] = ampweights

writefile.close()
