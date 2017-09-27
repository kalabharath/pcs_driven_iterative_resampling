#PBS -P xc4
#PBS -q normal
#PBS -l walltime=5:00:00
#PBS -l mem=2000GB
#PBS -l ncpus=1024
#PBS -l wd

#Load required module to run mpi compiled rosetta executables
module load openmpi

# Variable flags
################
# Change ./config.txt file
# Please change the executable and database paths according to your operating system.
# For arg1 and arg2, give input 9 and 3 residue fragment library files.
# For arg3, give the target protein starting model in pdb format.
# For arg4, give input broker file.
# For arg5, give number of structures to generate, typically 1,000 structures are needed. Atleast generate 100.
# For arg6, give the ouput silent file name.
# For arg7, give output score file name.

Executable_path=$(sed -n '2p' config.txt)
Executable="$(cut -d'=' -f2 <<<"$Executable_path")"
database_path=$(sed -n '5p' config.txt)
database="$(cut -d'=' -f2 <<<"$database_path")"
database="-database $database"
protein=$(sed -n '6p' config.txt)
protein="$(cut -d'=' -f2 <<<"$protein")"
arg1="-abinitio::increase_cycles 4.0"
arg2="-abinitio::rg_reweight 0.5 -abinitio::rsd_wt_helix 0.5 -abinitio::rsd_wt_loop 0.5 -abinitio::use_filters false"
arg3="-nstruct 1022"
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
broker_flag="-broker::setup ../setup/broker.txt -run:protocol broker -overwrite"
mpirun="mpirun -np 1024"

run="$mpirun $Executable $database $arg1 $arg2 $arg3 $arg4 $arg5 $arg6 $arg7 $arg8 $patch_flag $broker_flag $exclude"
echo $run
$run

qsub auto_extract_relax.sh"
