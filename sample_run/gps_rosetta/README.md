# Setup Fragment files </br>

Rename 9mer and 3 mer fragment libraries (aat000_09_06.200_v1_3 , aat000_03_06.200_v1_3) to 'frag9_1h68_r0.tab'  and 'frag3_1h68_r0.tab'.  </br>
Eg: for your own target it should be of the format "frag9_PDBID_r0.tab". The "r0" in the file name suggests that these are default fragments 
to be used for 'round zero'. The fragment libraries for the subsequent rounds are generated automatically. 

# Setup 'Config.txt' </br>
The config file is where you setup your total number of GPS-Rosetta iterations. The config file only contains 4 lines. </br>
*1. line is the description. do not edit or delete this line. </br> 
*2. Place holder (or) pdbid. Should match the 'PDBID' descriptor as in the fragment files. eg: 'frag9_1h68_r0.tab', where 'PDBID is '1h68'. </br>
*3. Current iteration, defaults to zero (0). This number updates automatically with increase in iteration by the algorithm. However, if you want to restart your run from any iteration, modify the line to any number. </br>
*4. Total number of iterations to run GPS-Rosetta. The algorithm quits automatically when it reaches convergence (or) it iterates to a total number of specified
iterations as given here. Defaults to ten iterations.</br>