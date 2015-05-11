import sys, os
protein=(os.popen("sed -n '1p' config.txt").read()).rstrip()
iter=(os.popen("sed -n '3p' config.txt").read()).rstrip()
EXECUTABLE="/short/xc4/kbp502/gps4rosetta/Rosetta/main/source/bin/score.linuxgccrelease"
BROKER_FLAG="-broker::setup ../setup/broker-ts3.txt -run:protocol broker -overwrite"
DATABASE="-database /short/xc4/kbp502/gps4rosetta/Rosetta/main/database"
FULL="-in:file:silent ./"+protein+".silent_file"
WEIGHTS="-score:weights pcsweight.patch"
NATIVE="-in:file:native ../setup/idealized_"+protein+".pdb"
OUT="-out:file:scorefile "+protein+"_1_pcs.csc"
MPI="mpirun -np 2"

print EXECUTABLE, DATABASE, WEIGHTS, NATIVE, OUT, FULL, BROKER_FLAG

os.system(str(MPI)+" "+str(EXECUTABLE)+" " +str(DATABASE)+" "+str(WEIGHTS)+" "+str(NATIVE)+" "+str(OUT)+" "+str(FULL)+" "+str(BROKER_FLAG))
