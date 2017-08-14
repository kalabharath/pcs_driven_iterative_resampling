import sys, os,time

def setup_variables():
    global silentfile, protein, max_iter, current_iter
    config=open('config.txt','r')
    protein=str(config.readline())    
    max_iter=int(config.readline())    
    current_iter=int(config.readline())
    config.close()      
    protein=protein.rstrip()
    silentfile = "relax_top_"+protein+"_r"+str(current_iter)+".silent_file"

setup_variables()
filein=open(silentfile,'r')
lines=filein.readlines()
filein.close()

rescore_file="pcs_"+protein+"_relax_top_rescore_r"+str(current_iter)+".fsc"
rescore_filein=open(rescore_file,'r')
scorelines=rescore_filein.readlines()
rescore_filein.close()

score_dict={}
wts_file=protein+"_r"+str(current_iter)+".wts"
fin = open(wts_file,'r')
wts = fin.readlines()
current_wts = []
for wt in wts:
    tag, wf = wt.split("=")
    current_wts.append(float(wf))
    
for i in range(1,len(scorelines)):    
    sline=scorelines[i].split()
    """
    ### PCS+Rosetta score
    if sline[0]=='SCORE:':
        score_dict[float(sline[1])]=sline[-1][:-5]
        
    
    # PCS only score
    if sline[0]=='SCORE:':
        score_dict[float(sline[7])+float(sline[8])+float(sline[9])+float(sline[10])]=sline[-1][:-5]
    """
    
    # use normalised pcs
        
    if sline[0]=='SCORE:':
        score_dict[float(sline[7])/current_wts[0]+float(sline[8])/current_wts[1]+float(sline[9])/current_wts[2]+float(sline[10])/current_wts[3]]=sline[-1][:-5]
    else:
        exit()
    
scores=score_dict.keys()
scores.sort()

top_100=[]
for j in range(0,100):
    decoy=score_dict[scores[j]]
    top_100.append(decoy)

print top_100

fileout=open(str("top_")+silentfile,'w')

for x in range (0,2):    
    fileout.write(lines[x])

for i in range(2,len(lines)):
    line=lines[i].split()    
    if (line[0]=='SCORE:') and (line[-1] in top_100):                        
        fileout.write(lines[i])
        i=i+1
        line=lines[i].split()    
        while (line[0]!='SCORE:'):            
            fileout.write(lines[i])            
            i=i+1
            if i==len(lines):
                break
            else:
                line=lines[i].split()
            

fileout.close()
time.sleep(60)
exit()
