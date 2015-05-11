import sys,os,glob

import pymol
pymol.pymol_argv = [ 'pymol', '-qc'] # Quiet and no GUI
pymol.finish_launching()
"""
if not os.path.exists('aligned'): os.mkdir('aligned')
else:
    os.system("rm -rf aligned")
    os.mkdir('aligned')

pymol.cmd.load('S_07577.pdb','best')

os.chdir("../228_stripped_20k_pdbs/")
for file in glob.glob("*.pdb"):
    print file
    pymol.cmd.load(file,file[:-5])
    pymol.cmd.align(file[:-5],'best')
    pymol.cmd.save("/local/kalabharath/DVP_Local/abrelax_2mutants/movie/aligned/"+file,file[:-5],state=0)
    pymol.cmd.delete(file[:-5])


pymol.cmd.reinitialize()
"""

#pymol.cmd.set("antialias =1")
pymol.cmd.set ('antialias','1','', 0,1, 1)
#pymol.cmd.set(string antialias,1)
pymol.cmd.set ('ambient',"0.3",'',0,1,1)
pymol.cmd.set ("light_count","6",'',0,1,1)

#   stick_radius -adjust thickness of atomic bonds
pymol.cmd.set ('stick_radius','0.6','',0,1,1)
pymol.cmd.set ('sphere_scale','0.5','',0,1,1)
pymol.cmd.set ('cartoon_rect_width','0.9','',0,1,1)
pymol.cmd.set ('cartoon_rect_length','2.0','',0,1,1)
pymol.cmd.set ('cartoon_loop_radius','0.5','',0,1,1)
#   mesh_radius -to adjust thickness of electron
#   density contours
pymol.cmd.set('mesh_radius',' 0.02','',0,1,1)

#   bg_color --pymol.cmd.set the background color
#pymol.cmd.set('bg_color','white','',0,1,1)

fin=open('config.txt','r')
protein=fin.readline().rstrip()
fin.close()

pymol.cmd.bg_color("white")

ideal_file = "../setup/idealized_"+protein+".pdb"
state=1
pymol.cmd.load(ideal_file,"obj1")
pymol.cmd.show_as('cartoon')
pymol.cmd.color('grey')

state+=1

pdb_in=''

for file in glob.glob("*.pdb"):
    pdb_in=file

print pdb_in
pymol.cmd.load(pdb_in, "obj2")
pymol.cmd.show_as('cartoon')
pymol.cmd.color('red', "obj2")
pymol.cmd.align("obj1","obj2")

pymol.cmd.center()
pymol.cmd.orient()
pymol.cmd.zoom()
pymol.cmd.mset('1 - %d' % pymol.cmd.count_states())
"""
pymol.cmd.set_view='(\
     0.017624758,   -0.997306943,   -0.071203344,\
    -0.656398058,    0.042179316,   -0.753232718,\
     0.754207492,    0.060014214,   -0.653885424,\
     0.000000950,   -0.000033716, -206.950531006,\
    45.939758301,   43.484542847,   46.991050720,\
   159.799530029,  216.515686035,    0.000000000 ,'',0,1,1)'
### cut above here and paste into script ###
"""
pymol.cmd.show_as('cartoon')

#set ray_trace_mode','3
# pymol.cmd.viewport(700,500)
pymol.cmd.viewport(2000,1000)

#### make output directory (NOTE: preceeding '/' ',' literal python,'',0,1,1)
pymol.cmd.set('ray_trace_frames','1','',0,1,1)
pymol.cmd.set('cache_frame','0','',0,1,1)
outfile = protein+"_superimpose"
pymol.cmd.mpng(outfile)
cp_file = "cp *_superimpose*.png ../../"

os.system(cp_file)
