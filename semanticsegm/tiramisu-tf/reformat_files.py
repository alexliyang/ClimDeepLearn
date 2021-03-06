import numpy as np
import h5py as h5
import os

#path
input_path="/gpfs/alpinetds/scratch/tkurth/csc190/segm_h5_v3"
output_path="/gpfs/alpinetds/scratch/tkurth/csc190/segm_h5_v3_reformat"

#create output path if not exists
if not os.path.isdir(output_path):
    os.makedirs(output_path)

#look for labels and data files
labelfiles = sorted([x for x in os.listdir(input_path) if x.startswith("label")])
datafiles = sorted([x for x in os.listdir(input_path) if x.startswith("data")])
outfiles = sorted([x for x in os.listdir(output_path) if x.startswith("data")])

#only use the data where we have labels for and vice versa
datafiles = sorted([x for x in datafiles if x.replace("data","labels") in labelfiles and not x in outfiles])
labelfiles = sorted([x for x in labelfiles if x.replace("labels","data") in datafiles and not x.replace("labels","data") in outfiles])

#iterate over files and write
for datafile,labelfile in zip(datafiles,labelfiles):
    print("Working on {} {}".format(datafile,labelfile))

    #data
    with h5.File(input_path+"/"+datafile,"r") as f:
        data = np.transpose(f["climate"]["data"][...],[2,0,1]).astype(np.float32)
        data_stats = np.transpose(f["climate"]["data_stats"][...],[1,0]).astype(np.float32)
    #label
    with h5.File(input_path+"/"+labelfile,"r") as f:
        labels = f["climate"]["labels"][...].astype(np.int32)
  
    #data
    with h5.File(output_path+'/'+datafile,'w',libver="latest") as f:
        #create group
        f.create_group("climate")
        #create data dataset
        dset_d = f.create_dataset("climate/data", (16,768,1152), chunks=(16,768,1152))
        dset_d[...] = data[...]
        #create labels dataset
        dset_l = f.create_dataset("climate/labels", (768,1152), chunks=(768,1152))
        dset_l[...] = labels[...]
        #create stats dataset
        dset_s = f.create_dataset("climate/stats", (16,4), chunks=(16,4))
        dset_s[...] = data_stats[...]
