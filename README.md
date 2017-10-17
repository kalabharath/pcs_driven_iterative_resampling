# Pseudocontact shift-driven iterative resampling for 3D structure determinations of large proteins </br>
# Abstract </br>
Pseudocontact shifts (PCSs) induced by paramagnetic lanthanides produce pronounced effects in nuclear magnetic resonance spectra, which are easily measured and which deliver valuable long-range structure restraints. Even sparse PCS data greatly enhance the success rate of 3D (3-dimensional) structure predictions of proteins by the modeling program Rosetta. The present work extends this approach to 3D structures of larger proteins, comprising more than 200 residues, which are difficult to model by Rosetta without additional experimental restraints. The new algorithm improves the fragment assembly method of Rosetta by utilizing PCSs generated from paramagnetic lanthanide ions attached at four different sites as the only experimental restraints. The sparse PCS data are utilized at multiple stages, to identify native-like local structures, to rank the best structural models and to rebuild the fragment libraries. The fragment libraries are refined iteratively until convergence. The PCS-driven iterative resampling algorithm is strictly data dependent and shown to generate accurate models for a benchmark set of eight different proteins, ranging from 100 to 220 residues, using solely PCSs of backbone amide protons. </br>
# Reference article

Pseudocontact shift-driven iterative resampling for 3D structure determinations of large proteins </br>
KB Pilla, G Otting, T Huber </br>
Journal of molecular biology 428 (2), 522-532 </br>

download the article from http://www.sciencedirect.com/science/article/pii/S0022283616000267 (or) http://kalabharath.github.io/ </br>
# Running the algorithm

See the README files in all of the folders in the "./sample_run" for detailed explanation of different files and scripts needed for running the protocol. Please modify all of the relevant files for your own protein system. </br>

# Dependencies
-Rosetta, any version from 2015 - till date. Last tested on version 3.8. </br>
 Download from https://www.rosettacommons.org/software/academic </br>
-Compile Rosetta on any cluster or supercomputer with MPI enabled. </br>
-Python 2.7 </br>
-The current scripts are written for PBS load balancer. </br>

# Support
For any of your questions on using PCSs in Rosetta, please email me at kalabharath@gmail.com </br>
