try:import sys
except:pass
f=open('D:\programacion\sublime3\Data\Packages/temporal.txt', 'w')
for m in dir(sys): f.write(m+'\n')
f.close()