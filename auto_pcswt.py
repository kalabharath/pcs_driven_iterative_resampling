import sys, os

protein=(os.popen("sed -n '1p' config.txt").read()).rstrip()
os.system("mv score.fsc score_cs.fsc")
cs_rosetta=open("score_cs.fsc", 'r')
pcs_1f=open(protein+"_1_pcs.csc", 'r')
output=open(protein+"_r0.wts",'w',1)
output1=open(protein+"_score12.wts",'w',1)

"""
SCORE, score, vdw, cenpack, pair, env, cbeta, rg, hs_pair, ss_pair, rsigma, sheet, co, rms, maxsub, clashes_total, clashes_bb, time_description
"""

cs_rosetta.readline()
csline=cs_rosetta.readline()

cs_score= []
pcs_score=[]


while(csline):
#    SCORE,     score,        vdw,    cenpack,       pair,        env,      cbeta,         rg,    hs,_pair,    ss_pair,     rsigma,      sheet,    co,        rms,     maxsub,    clashes_total,    clashes_bb,       time, description = csline.split()j
    try:
        
        SCORE, score, vdw, cenpack, pair, env, cbeta, rg, hs_pair, ss_pair, rsigma, sheet, co, rms, maxsub, clashes_total, clashes_bb, time, description = csline.split()
        cs_score.append(float(score))
        csline=cs_rosetta.readline()
    except:
        SCORE, score,        vdw,    cenpack,       pair,    atom_pair_constraint,    angle_constraint,    dihedral_constraint,        env,      cbeta,         rg,    hs_pair,    ss_pair,     rsigma,      sheet,    co,        rms,     maxsub,    clashes_total,    clashes_bb,       time, description  = csline.split()
        cs_score.append(float(score))
        csline=cs_rosetta.readline()


cs_rosetta.close()
pcs_1f.readline()
pcs_ts1=[]
pcs_ts2=[]
pcs_ts3=[]
pcs_ts4=[]

pcsline=pcs_1f.readline()

while(pcsline):
    try:
        SCORE,     score,     pcsTs1,     pcsTs2,     pcsTs3, pcsTs4,    Filter_Stage2_aBefore,    Filter_Stage2_bQuarter,    Filter_Stage2_cHalf,    Filter_Stage2_dEnd,    allatom_rms,    gdtmm,    gdtmm1_1,    gdtmm2_2,    gdtmm3_3,    gdtmm4_3,    gdtmm7_4,    irms,    loop_chain_score,    loop_overlap_score,    loop_total_score,    loop_vdw_score,    looprms,    maxsub,    maxsub20,    rms,    silent_score,    srms,    time, description = pcsline.split()
    except:
        SCORE, score,  pcsTs1,  pcsTs2,  pcsTs3, pcsTs4, allatom_rms, clashes_bb, clashes_total, gdtmm, gdtmm1_1, gdtmm2_2, gdtmm3_3, gdtmm4_3, gdtmm7_4, irms, maxsub, maxsub2, rms, silent_score, srms, time, description = pcsline.split()
    pcs_score.append(float(score))   
    pcs_ts1.append(float(pcsTs1))
    pcs_ts2.append(float(pcsTs2))
    pcs_ts3.append(float(pcsTs3))
    pcs_ts4.append(float(pcsTs4))
    pcsline=pcs_1f.readline()


pcs_1f.close()

#sort all arrays in ascending order

cs_score.sort()
pcs_ts1.sort()
pcs_ts2.sort()
pcs_ts3.sort()
pcs_ts4.sort()

cs_low=0
cs_high=0

for i in range (1,101):
    cs_low = cs_low+cs_score[i-1]
    a_low=cs_low/(100.00)
    cs_high =cs_high+cs_score[-1*(i)]
    a_high=cs_high/(100.00)
    
pcs_weights=[]
pcs_low=0
pcs_high=0

for j in range (1,101):
    pcs_low = pcs_low + pcs_ts1[j-1]
    c_low=pcs_low/(100.00)
    pcs_high =pcs_high + pcs_ts1[-1*(j)]
    c_high=pcs_high/(100.00)
pcs_weights.append((a_high-a_low)/(c_high-c_low))

pcs_low=0
pcs_high=0

for j in range (1,101):
    pcs_low = pcs_low + pcs_ts2[j-1]
    c_low=pcs_low/(100.00)
    pcs_high =pcs_high + pcs_ts2[-1*(j)]
    c_high=pcs_high/(100.00)
pcs_weights.append((a_high-a_low)/(c_high-c_low))

pcs_low=0
pcs_high=0

for j in range (1,101):
    pcs_low = pcs_low + pcs_ts3[j-1]
    c_low=pcs_low/(100.00)
    pcs_high =pcs_high + pcs_ts3[-1*(j)]
    c_high=pcs_high/(100.00)
pcs_weights.append((a_high-a_low)/(c_high-c_low))
    
pcs_low=0
pcs_high=0

for j in range (1,101):
    pcs_low = pcs_low + pcs_ts4[j-1]
    c_low=pcs_low/(100.00)
    pcs_high =pcs_high + pcs_ts4[-1*(j)]
    c_high=pcs_high/(100.00)
pcs_weights.append((a_high-a_low)/(c_high-c_low))
    

x=0        
for entry in pcs_weights:
    x=x+1
    tmp2=round((entry/4),3)
    print entry
    print tmp2
    tmp= "pcsTs"+str(x)+" = "+str(tmp2)+"\n"
    output.write(tmp)
x=0
output1.write("METHOD_WEIGHTS ref  0.16 1.7 -0.67 -0.81 0.63 -0.17 0.56 0.24 -0.65 -0.1 -0.34 -0.89 0.02 -0.97 -0.98 -0.37 -0.27 0.29 0.91 0.51 \n")
for entry in pcs_weights:
    x=x+1
    tmp2=round((entry/4),3)
    print entry
    print tmp2
    tmp= "pcsTs"+str(x)+"  "+str(tmp2)+"\n"
    output1.write(tmp)
output.close()
output1.close()
