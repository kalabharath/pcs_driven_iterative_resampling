import sys, os

def generatePatchFile(broker_file):
    with open(broker_file) as fin:
        lines = fin.readlines()
    count = 0
    for line in lines:
        if 'CLAIMER PseudocontactShiftEnergyController' in line:
            count += 1
    if count:
        with open('pcsweight.patch','w') as fout:
            fout.write("METHOD_WEIGHTS ref  0.16 1.7 -0.67 -0.81 0.63 -0.17 0.56 0.24 -0.65 -0.1 -0.34 -0.89 0.02 -0.97 -0.98 -0.37 -0.27 0.29 0.91 0.51 \n")
            for i in range(0,count):
                outline='pcsTs'+str(i+1)+" 1.0 \n"
                fout.write(outline)
    return True

def calc_weight(broker_t):
    broker_line = ''
    for entry in broker_t:
        broker_line = broker_line+entry+" "

    protein=(os.popen("sed -n '5p' config.txt").read()).rstrip()
    protein = protein.split("=")
    protein = protein[1]
    iter=(os.popen("sed -n '7p' config.txt").read()).rstrip()
    iter = iter.split("=")
    iter = iter[1]
    exe_path=(os.popen("sed -n '3p' config.txt").read()).rstrip()
    exe_path = exe_path.split("=")
    exe_path = exe_path [1]
    broker_flag=broker_line
    database_path = (os.popen("sed -n '4p' config.txt").read()).rstrip()
    database_path = database_path.split("=")
    database_path = '-database '+database_path[1]
    full="-in:file:silent ./"+protein+".silent_file -mute all"
    weights="-score:weights pcsweight.patch"
    native="-in:file:native ../setup/idealized_"+protein+".pdb"
    out="-out:file:scorefile "+protein+"_1_pcs.csc"
    mpi="mpirun -np 2"

    print mpi, exe_path, database_path, weights, native, out, full, broker_flag
    run_score = mpi+" "+exe_path+" "+database_path+" "+weights+" "+native+" "+out+" "+full+" "+broker_flag
    os.system(run_score)
    return True

if __name__ == '__main__':
    #sys.argv = ['auto_rescore.py', '-broker::setup', '../setup/broker-ts3.txt', '-run:protocol', 'broker', '-overwrite']
    generatePatchFile(sys.argv[2])
    calc_weight(sys.argv[1:])
