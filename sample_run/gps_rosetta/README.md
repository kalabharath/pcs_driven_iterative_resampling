# Setup Fragment files </br>

Rename 9mer and 3 mer fragment libraries (aat000_09_06.200_v1_3 , aat000_03_06.200_v1_3) to 'frag9_1h68_r0.tab'  and 'frag3_1h68_r0.tab'.  </br>
Eg: for your own target it should be of the format "frag9_PDBID_r0.tab". The "r0" in the file name suggests that these are default fragments 
to be used for 'round zero'. The fragment libraries for the subsequent rounds are generated automatically. 

# Setup 'Config.txt' </br>
Ideally the "config.txt" is the only file that you need to modify to carry out the iterative-GPS Rosetta protocol. </br>
1. The path to your minirosetta.mpi.linuxgccrelease executable </br>
2. The path to your score.mpi.linuxgccrelease executable </br>
3. The path to your relax.mpi.linuxgccrelease executable </br>
4. The path to your Rosetta database </br>
5. Place holder (or) pdbid. Should match the 'PDBID' descriptor as in the fragment files. eg: 'frag9_1h68_r0.tab', where 'PDBID is '1h68'. </br>
6. Total number of iterations to run GPS-Rosetta. The algorithm quits automatically when it reaches convergence (or) it iterates to a total number of specified iterations as given here. </br>
7. Current iteration, defaults to zero (0). This number updates automatically with increase in iteration by the algorithm. However, if you want to restart your run from any iteration, modify the line to desired iteration. </br>

# Modify the headers in all of the ".sh" files </br>
You have to modify the headers to match the headers for the job queuing system on your super computer. especially walltime and ncpus. The given headers work on "NCI's Raijin" </br>
"#PBS -P xc4" </br>
"#PBS -q normal" </br>
"#PBS -l walltime=6:00:00" </br>
"#PBS -l mem=2000GB" </br>
"#PBS -l ncpus=1024" </br>
"#PBS -l wd" </br>
"#Load required module to run mpi compiled rosetta executables" </br>
"module load openmpi" </br>
Also change the "mpirun" variable to match the ncpus </br>

# The Algorithm is encoded in four ".sh" files: 

Submit the auto_cs.sh to the job queing system. The algorithm runs and terminates automatically, provided that sufficient wall times are specified in the ".sh" files. </br>
![Screenshot](https://raw.githubusercontent.com/kalabharath/pcs_driven_iterative_resampling/master/sample_run/gps_rosetta/iterGPSrosetta.png)

# Termination
Upon reaching convergence (where the PCS energy is not dropped any further), the program automatically exits and generates the top10 lowest energy scoring decoys in pdb format and the corresponding ranking of the decoys is shown in the file "Final_results.txt" </br>
If you want to run a specific number of iterations and not to check for convergence, delete or comment lines 235 and 236 in the file "auto_silent2database.py"