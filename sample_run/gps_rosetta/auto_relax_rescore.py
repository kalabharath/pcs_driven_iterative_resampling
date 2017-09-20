import sys, os
def rescore_with_pcs():
    protein = (os.popen("sed -n '6p' config.txt").read()).rstrip()
    protein = protein.split("=")
    protein = protein[1]
    iter = (os.popen("sed -n '8p' config.txt").read()).rstrip()
    iter = iter.split("=")
    iter = iter[1]
    exe_path=(os.popen("sed -n '3p' config.txt").read()).rstrip()
    exe_path = exe_path.split("=")
    exe_path = exe_path [1]
    broker_flag="-broker::setup ../setup/broker.txt -run:protocol broker -overwrite"
    database_path = (os.popen("sed -n '5p' config.txt").read()).rstrip()
    database_path = database_path.split("=")
    database_path = '-database '+database_path[1]
    full="-in:file:fullatom -in:file:silent ./relax_top_"+protein+"_r"+iter+".silent_file"
    weights="-score:weights "+ protein+"_relax.wts"
    native="-in:file:native ../setup/idealized_"+protein+".pdb"
    out="-out:file:scorefile pcs_"+protein+"_relax_top_rescore_r"+iter+".fsc -mute all"
    mpi="mpirun -np 2"

    print mpi, exe_path, database_path, weights, native, out, full, broker_flag
    run_score = mpi+" "+exe_path+" "+database_path+" "+weights+" "+native+" "+out+" "+full+" "+broker_flag
    os.system(run_score)
    return True

if __name__ == '__main__':
   rescore_with_pcs()
