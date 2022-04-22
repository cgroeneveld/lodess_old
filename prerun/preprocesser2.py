import numpy as np
import multiprocessing as mp
import sys,os,glob,shutil

def _trymakeDir(dirname):
    try:
        os.mkdir(dirname)
    except:
        shutil.rmtree(dirname)
        os.mkdir(dirname)

def process_lnum(tup):
    lnum = tup[0]
    data = tup[1]
    _trymakeDir(lnum)
    os.chdir(lnum)
    matches = np.array([lnum in st for st in data])
    links = np.array(data)[matches]
    links = [link.rstrip('\n') for link  in links]

    sbnums = ['SB'+link.split('SB')[1][:3] for link in links]
    succesful = [False] * len(links) # Start of with no files downloaded

    while np.sum(np.array(succesful)) < len(links): # Still files to be processed...
        todo = np.logical_not(np.array(succesful,dtype=bool))
        selected_links = np.array(links)[todo]
        commands = [f'wget -c --timeout=10 --tries=15 "{name}"' for name in selected_links]
        for com in commands:
            os.system(com)
        
        for sb in np.array(sbnums)[todo]: # To make life easier when deciding what to untar
            try:
                name = glob.glob(f'*{sb}*tar')[0]
                call = f'tar --force-local -xvf {name}'
                os.system(call)
                index = np.where(np.array(sbnums) == sb)[0][0]
                succesful[index] = True
                os.remove(name)
            except:
                try:
                    msfile = glob.glob(f'*{sb}*MS')[0]
                    shutil.rmtree(msfile)
                except:
                    pass
    os.chdir('..')
    return(0)
    

def main(args):
    numthreads = 4
    pl = mp.Pool(numthreads)
    txtfile = args[1]
    data = []
    with open(txtfile,'r') as handle:
        for line in handle:
            data.append(line)
    lnums = np.array([lin.split('/')[-1].split('_')[0] for lin in data])
    lnums_unique = np.unique(lnums)
    process_tups = [(lnum,data) for lnum in lnums_unique]
    _ = list(pl.map(process_lnum,process_tups))


if __name__ == '__main__':
    main(sys.argv)