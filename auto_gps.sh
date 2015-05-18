#PBS -P xc4
#PBS -q normal
#PBS -l walltime=5:00:00
#PBS -l mem=2000GB
#PBS -l ncpus=1024
#PBS -l wd

module load openmpi

Executable="/short/xc4/kbp502/gps4rosetta/Rosetta/main/source/bin/minirosetta.mpi.linuxgccrelease"
database="-database /short/xc4/kbp502/gps4rosetta/Rosetta/main/database"
protein=$(sed -n '1p' config.txt)
arg1="-abinitio::increase_cycles 5"
arg2="-abinitio::rg_reweight 0.5 -abinitio::rsd_wt_helix 0.5 -abinitio::rsd_wt_loop 0.5 -abinitio::use_filters false"
arg3="-nstruct 2046"
arg4="-mute all"
arg5="-frag9 ./frag9_${protein}_r0.tab"
arg6="-frag3 ./frag3_${protein}_r0.tab"
arg7="-in:file:native ../setup/idealized_$protein.pdb"
arg8="-out::file:silent ${protein}_r0.silent_file"
patch1="-abinitio::stage1_patch ${protein}_r0.wts"
patch2="-abinitio::stage2_patch ${protein}_r0.wts"
patch3="-abinitio::stage3a_patch ${protein}_r0.wts"
patch4="-abinitio::stage3b_patch ${protein}_r0.wts"
patch5="-abinitio::stage4_patch ${protein}_r0.wts"

patch_flag="$patch1 $patch2 $patch3 $patch4 $patch5"
broker_flag="-broker::setup ../setup/broker-ts34.txt -run:protocol broker -overwrite"
mpirun="mpirun -np 1024"
run="$mpirun $Executable $database $arg1 $arg2 $arg3 $arg4 $arg5 $arg6 $arg7 $arg8 $arg9 $arg10 $patch_flag $broker_flag $exclude"
echo $run
$run

qsub auto_extract_relax.sh
