import sys,os

f=open('config.txt','r')

protein=f.readline().rstrip()
f.close()

print protein
for i in range(0,11):
    ex="grep SCORE "+protein+"_r"+str(i)+".silent_file > temp"+str(i)+".csc"
    print ex
    os.system(ex)

plot = "plot 'temp0.csc' using 28:2 with points,"
print plot

for i in range(1,11):
    plot = plot+" 'temp"+str(i)+".csc' using 28:2 with points,"

print plot
