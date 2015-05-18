import sys, os

protein=(os.popen("sed -n '1p' config.txt").read()).rstrip()
iter=(os.popen("sed -n '3p' config.txt").read()).rstrip()

wts_in=protein+"_r"+iter+".wts"
fin=open(wts_in,'r')
wts=fin.readlines()
fin.close()
score12= protein+'_r'+iter+"_talaris2013.wts"
copy_12="cp talaris2013.wts "+score12
os.system(copy_12)
score12_in=open(score12,'a')
for wt in wts:
    pcsst,equal,wt_factor=wt.split()
    outline=pcsst+" "+wt_factor
    score12_in.write(outline)
    score12_in.write('\n')
score12_in.close()

EXECUTABLE="/short/xc4/kbp502/gps4rosetta/Rosetta/main/source/bin/score.linuxgccrelease"
BROKER_FLAG="-broker::setup ../setup/broker-ts34.txt -run:protocol broker -overwrite"
DATABASE="-database /short/xc4/kbp502/gps4rosetta/Rosetta/main/database"
FULL="-in:file:fullatom -in:file:silent ./relax_top_"+protein+"_r"+iter+".silent_file"
WEIGHTS="-score:weights "+score12
NATIVE="-in:file:native ../setup/idealized_"+protein+".pdb"
OUT="-out:file:scorefile pcs_"+protein+"_relax_top_rescore_r"+iter+".fsc"
MPI="mpirun -np 2"

print EXECUTABLE, DATABASE, WEIGHTS, NATIVE, OUT, FULL, BROKER_FLAG

os.system(str(MPI)+" "+str(EXECUTABLE)+" " +str(DATABASE)+" "+str(WEIGHTS)+" "+str(NATIVE)+" "+str(OUT)+" "+str(FULL)+" "+str(BROKER_FLAG))

