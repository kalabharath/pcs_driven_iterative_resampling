import sys, os,time

def setup_variables():
    global silentfile, protein, max_iter, current_iter
    config=open('config.txt','r')
    protein=str(config.readline())    
    max_iter=int(config.readline())    
    current_iter=int(config.readline())
    config.close()      
    protein=protein.rstrip()
    silentfile = protein+str("_r")+str(current_iter)+str(".silent_file")

setup_variables()
filein=open(silentfile,'r')
lines=filein.readlines()
filein.close()

wts_file=protein+"_r"+str(current_iter)+".wts"
fin = open(wts_file,'r')
wts = fin.readlines()
current_wts = []
for wt in wts:
    tag, wf = wt.split("=")
    current_wts.append(float(wf))   

print silentfile
score_dict={}
for i in range(2,len(lines)):    
    sline=lines[i].split()
    
    """
    # use pcs+centroid
    if sline[0]=='SCORE:':        
        score_dict[float(sline[1])]=sline[-1]
    
    
    # use pcs alone
    if sline[0]=='SCORE:':    
        score_dict[float(sline[2])+float(sline[3])+float(sline[4])+float(sline[5])]=sline[-1]
    """
    # use normalised pcs
    
    if sline[0]=='SCORE:':    
        score_dict[float(sline[2])/current_wts[0]+float(sline[3])/current_wts[1]+float(sline[4])/current_wts[2]+float(sline[5])/current_wts[3]]=sline[-1]
        

fileout=open(str("top_")+silentfile,'w')

scores=score_dict.keys()
scores.sort()

top_200=[]

for j in range(0,200):
    decoy=score_dict[scores[j]]
    top_200.append(decoy)

print top_200

for x in range (0,2):    
    fileout.write(lines[x])

for i in range(2,len(lines)):
    line=lines[i].split()    
    if (line[0]=='SCORE:') and (line[-1] in top_200):                        
        fileout.write(lines[i])
        i=i+1
        line=lines[i].split()    
        while (line[0]!='SCORE:'):
            fileout.write(lines[i])
            i=i+1
            line=lines[i].split()    

fileout.close()
time.sleep(60)
exit()

