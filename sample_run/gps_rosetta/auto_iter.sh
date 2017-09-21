#PBS -P xc4
#PBS -q normal
#PBS -l walltime=5:00:00
#PBS -l mem=2000GB
#PBS -l ncpus=1024
#PBS -l wd

module load openmpi

Executable_path=$(sed -n '2p' config.txt)
Executable="$(cut -d'=' -f2 <<<"$Executable_path")"
database_path=$(sed -n '5p' config.txt)
database="$(cut -d'=' -f2 <<<"$database_path")"
database="-database $database"
protein=$(sed -n '6p' config.txt)
protein="$(cut -d'=' -f2 <<<"$protein")"
iter=$(sed -n '8p' config.txt)
iter="$(cut -d'=' -f2 <<<"$iter")"
arg1="-abinitio::increase_cycles 4.0"
arg2="-abinitio::rg_reweight 0.5 -abinitio::rsd_wt_helix 0.5 -abinitio::rsd_wt_loop 0.5 -abinitio::use_filters false"
arg3="-nstruct 2044"
arg4="-mute all"
arg5="-frag9 ./frag9_${protein}_r${iter}.tab"
arg6="-frag3 ./frag3_${protein}_r${iter}.tab"
arg7="-out::file:silent ${protein}_r${iter}.silent_file"
arg8="-native ../setup/idealized_$protein.pdb"

patch1="-abinitio::stage1_patch ${protein}_r${iter}.wts"
patch2="-abinitio::stage2_patch ${protein}_r${iter}.wts"
patch3="-abinitio::stage3a_patch ${protein}_r${iter}.wts"
patch4="-abinitio::stage3b_patch ${protein}_r${iter}.wts"
patch5="-abinitio::stage4_patch ${protein}_r${iter}.wts"
patch_flag="$patch1 $patch2 $patch3 $patch4 $patch5"
broker_flag="-broker::setup ../setup/broker.txt -run:protocol broker -overwrite"

mpirun="mpirun -np 1024"
run="$mpirun $Executable $database $arg1 $arg2 $arg3 $arg4 $arg5 $arg6 $arg7 $arg8 $arg9 $arg10 $patch_flag $broker_flag"
echo $run
$run

new_job="qsub auto_extract_relax.sh"
echo $new_job
$new_job
